# Plan Bazy Danych ShelfSense

## 1. Lista Tabel

### `shelfsense.users`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `email` VARCHAR(254) NOT NULL UNIQUE
- `username` VARCHAR(255) NOT NULL
- `password_hash` VARCHAR(60) NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.books`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `title` VARCHAR(255) NOT NULL
- `author` VARCHAR(255) NOT NULL
- `isbn` VARCHAR(13) NULL
- `genre` TEXT NULL
- `description` TEXT NULL
- `publication_date` DATE NULL
- `page_count` INTEGER NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.user_preferences`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `user_id` UUID NOT NULL UNIQUE REFERENCES `shelfsense.users(id)` ON DELETE CASCADE
- `preferences_text` TEXT NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.user_library_entries`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `user_id` UUID NOT NULL REFERENCES `shelfsense.users(id)` ON DELETE CASCADE
- `book_id` UUID NOT NULL REFERENCES `shelfsense.books(id)` ON DELETE RESTRICT
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Constraint:** UNIQUE (`user_id`, `book_id`)
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.reviews`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `user_library_entry_id` UUID NOT NULL UNIQUE REFERENCES `shelfsense.user_library_entries(id)` ON DELETE CASCADE
- `review_text` TEXT NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.recommendations`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `user_id` UUID NOT NULL REFERENCES `shelfsense.users(id)` ON DELETE CASCADE
- `recommended_book_id` UUID NOT NULL REFERENCES `shelfsense.books(id)` ON DELETE RESTRICT
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Constraint:** UNIQUE (`user_id`, `recommended_book_id`)
- **Trigger:** `set_timestamp` BEFORE UPDATE

### `shelfsense.recommendation_ratings`
- `id` UUID PRIMARY KEY DEFAULT uuid_generate_v4()
- `recommendation_id` UUID NOT NULL UNIQUE REFERENCES `shelfsense.recommendations(id)` ON DELETE CASCADE
- `user_id` UUID NOT NULL REFERENCES `shelfsense.users(id)` ON DELETE CASCADE
- `rating` NUMERIC(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 5.0)
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- **Trigger:** `set_timestamp` BEFORE UPDATE

## 2. Relacje Między Tabelami

- `user_preferences` (user_id) 1:1 `users` (id) (ON DELETE CASCADE)
- `user_library_entries` (user_id) N:1 `users` (id) (ON DELETE CASCADE)
- `user_library_entries` (book_id) N:1 `books` (id) (ON DELETE RESTRICT)
- `reviews` (user_library_entry_id) 1:1 `user_library_entries` (id) (ON DELETE CASCADE)
- `recommendations` (user_id) N:1 `users` (id) (ON DELETE CASCADE)
- `recommendations` (recommended_book_id) N:1 `books` (id) (ON DELETE RESTRICT)
- `recommendation_ratings` (recommendation_id) 1:1 `recommendations` (id) (ON DELETE CASCADE)
- `recommendation_ratings` (user_id) N:1 `users` (id) (ON DELETE CASCADE)

## 3. Indeksy

- `idx_books_title` ON `shelfsense.books(title)`
- `idx_user_preferences_user_id` ON `shelfsense.user_preferences(user_id)`
- `idx_user_library_entries_user_id` ON `shelfsense.user_library_entries(user_id)`
- `idx_user_library_entries_book_id` ON `shelfsense.user_library_entries(book_id)`
- `idx_reviews_user_library_entry_id` ON `shelfsense.reviews(user_library_entry_id)`
- `idx_recommendations_user_id` ON `shelfsense.recommendations(user_id)`
- `idx_recommendations_recommended_book_id` ON `shelfsense.recommendations(recommended_book_id)`
- `idx_recommendation_ratings_recommendation_id` ON `shelfsense.recommendation_ratings(recommendation_id)`
- `idx_recommendation_ratings_user_id` ON `shelfsense.recommendation_ratings(user_id)`

## 4. Zasady PostgreSQL (Row Level Security)

- **Włączone RLS dla tabel:** `users`, `user_preferences`, `user_library_entries`, `reviews`, `recommendations`, `recommendation_ratings`.
- **Funkcja pomocnicza:** `shelfsense.current_user_id()` (zwraca UUID bieżącego użytkownika, wymaga implementacji w aplikacji).
- **Polityki:**
    - `user_manage_own` ON `users`: Użytkownik może zarządzać własnym rekordem (`FOR ALL USING (id = shelfsense.current_user_id())`).
    - `user_manage_own_preferences` ON `user_preferences`: Użytkownik może zarządzać własnymi preferencjami (`FOR ALL USING (user_id = shelfsense.current_user_id())`).
    - `user_manage_own_library_entries` ON `user_library_entries`: Użytkownik może zarządzać własnymi wpisami w bibliotece (`FOR ALL USING (user_id = shelfsense.current_user_id())`).
    - `user_manage_own_reviews` ON `reviews`: Użytkownik może zarządzać recenzjami powiązanymi z jego wpisami w bibliotece (`FOR ALL USING (EXISTS (SELECT 1 FROM shelfsense.user_library_entries ule WHERE ule.id = reviews.user_library_entry_id AND ule.user_id = shelfsense.current_user_id()))`).
    - `user_view_delete_own_recommendations` ON `recommendations`: Użytkownik może przeglądać i usuwać własne rekomendacje (`FOR SELECT, DELETE USING (user_id = shelfsense.current_user_id())`).
    - `user_manage_own_recommendation_ratings` ON `recommendation_ratings`: Użytkownik może zarządzać własnymi ocenami rekomendacji (`FOR ALL USING (user_id = shelfsense.current_user_id())`).

## 5. Dodatkowe Uwagi

- **Schema:** Wszystkie obiekty znajdują się w dedykowanym schemacie `shelfsense`.
- **Rozszerzenie:** Wymagane jest rozszerzenie `uuid-ossp` do generowania UUID.
- **Automatyczne `updated_at`:** Funkcja `shelfsense.trigger_set_timestamp()` i powiązane wyzwalacze automatycznie aktualizują kolumnę `updated_at` przy każdej modyfikacji wiersza.
- **Integralność danych:** Użyto `ON DELETE RESTRICT` dla kluczy obcych wskazujących na tabelę `books`, aby zapobiec usunięciu książki, jeśli jest ona w czyjejś bibliotece lub została zarekomendowana. Użyto `ON DELETE CASCADE` dla danych powiązanych z użytkownikiem, aby usunąć je wraz z kontem użytkownika.
- **Unikalność:** Zapewniono unikalność dla par (`user_id`, `book_id`) w `user_library_entries` oraz (`user_id`, `recommended_book_id`) w `recommendations`. Email użytkownika jest również unikalny.
- **Opcjonalne pola:** Niektóre pola w tabeli `books` (np. `isbn`, `genre`, `description`) są opcjonalne (`NULL`).
