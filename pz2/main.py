from classes import Administrator, RegularUser, GuestUser, AccessControl

# Авторство коду:
# Файл classes.py: Реалізація всіх класів написана власноруч.
# Файл main.py: Скрипт для тестування функціоналу згенеровано за допомогою Gemini 2.5

# --- Start of the verification script ---

# --- Початок коду для перевірки ---

# 1. Створення екземплярів різних користувачів
print("--- 1. Створення користувачів ---")
admin = Administrator('super_admin', 'adminpass', permissions=['read', 'write'])
active_user = RegularUser('john_doe', 'password123', is_active=True)
inactive_user = RegularUser('jane_doe', 'password456', is_active=False)
guest = GuestUser()

print(admin)
print(active_user)
print(inactive_user)
print(guest)
print("-" * 40)

# 2. Створення системи контролю доступу та додавання користувачів
print("--- 2. Додавання користувачів до системи AccessControl ---")
access_system = AccessControl()
access_system.add_user(admin)
access_system.add_user(active_user)
access_system.add_user(inactive_user)
access_system.add_user(guest)

# Спроба додати користувача, що вже існує
print("\nСпроба додати дублікат:")
access_system.add_user(RegularUser('john_doe', 'newpass', is_active=True))
print("-" * 40)


# 3. Тестування автентифікації
print("--- 3. Тестування автентифікації ---")

# --- Сценарій: Успішна автентифікація звичайного користувача ---
print("\n[Сценарій 1]: Успішна автентифікація для 'john_doe'")
print(f"  'john_doe' до входу: {access_system.users['john_doe']}")
authenticated_user = access_system.authenticate_user('john_doe', 'password123')
if authenticated_user:
    print(f"  Автентифікація успішна. Об'єкт: {authenticated_user}")
    print(f"  'john_doe' після входу: {access_system.users['john_doe']}")
else:
    print("  Автентифікація не вдалася.")

# --- Сценарій: Неправильний пароль ---
print("\n[Сценарій 2]: Неправильний пароль для 'super_admin'")
result = access_system.authenticate_user('super_admin', 'wrongpass')
print(f"  Результат: {result}")

# --- Сценарій: Неіснуючий користувач ---
print("\n[Сценарій 3]: Неіснуючий користувач 'unknown_user'")
result = access_system.authenticate_user('unknown_user', 'anypass')
print(f"  Результат: {result}")

# --- Сценарій: Вхід неактивного користувача ---
print("\n[Сценарій 4]: Вхід неактивного користувача 'jane_doe'")
result = access_system.authenticate_user('jane_doe', 'password456')
if result:
    # Цей блок тепер не повинен виконуватися
    print(f"  ПОМИЛКА: Автентифікація пройшла для неактивного користувача! Об'єкт: {result}")
else:
    print("  Автентифікація не вдалася, як і очікувалося для неактивного користувача.")

# --- Сценарій: Вхід для гостя ---
print("\n[Сценарій 5]: Спроба входу для гостя 'Guest'")
result = access_system.authenticate_user('Guest', '')
print(f"  Результат: {result} (очікувано, оскільки гості не мають пароля)")
print("-" * 40)


# 4. Тестування специфічних методів ролей
print("--- 4. Тестування специфічних методів ---")

# --- Адміністратор ---
print("\nПеревірка прав адміністратора 'super_admin':")
print(f"  Має право 'read'? -> {admin.has_permission('read')}")
print(f"  Має право 'delete'? -> {admin.has_permission('delete')}")
print("  Надаємо право 'delete'...")
admin.grant_permission('delete')
print(f"  Має право 'delete'? -> {admin.has_permission('delete')}")
print("  Забираємо право 'write'...")
admin.revoke_permission('write')
print(f"  Поточні права: {admin.permissions}")


# --- Гість ---
print("\nПеревірка сесії гостя:")
print(f"  Чи активна сесія гостя? -> {guest.is_session_active()}")

print("\n--- Перевірку завершено ---")