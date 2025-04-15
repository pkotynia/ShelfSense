##  Frontend
- React z TypeScript - dobry wybór zapewniający typowanie i stabilność kodu
- Material UI (jako jednolity system UI) - słuszne uproszczenie do jednego systemu UI
- React Query - dobry wybór do zarządzania stanem i zapytaniami, wystarczający na tym etapie
- Vite - nowoczesne i szybkie narzędzie buildowe

## Backend

- Python + FastAPI - szybki w implementacji i wydajny framework
- SQLAlchemy - solidny ORM upraszczający interakcje z bazą danych
- OpenAI SDK - wystarczające dla funkcji AI bez nadmiernej złożoności LangChain
- pytest - standard dla testów w Pythonie

## Baza Danych

- PostgreSQL (jedna baza) - wystarczające rozwiązanie dla MVP, eliminuje złożoność wielu baz
- Przechowywanie wszystkich danych w jednej bazie upraszcza architekturę

## Autoryzacja
- Własna implementacja JWT - odpowiednia dla MVP, eliminuje koszty zewnętrznych usług
- Hashowanie haseł (bcrypt) - zapewnia podstawowe bezpieczeństwo danych
Sesje użytkowników - niezbędna funkcjonalność do zarządzania stanem zalogowania