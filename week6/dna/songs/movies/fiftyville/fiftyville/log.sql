SELECT description FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

SELECT name, transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

SELECT name FROM people JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25 AND activity = 'exit';

SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);

SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE flight_id = (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
