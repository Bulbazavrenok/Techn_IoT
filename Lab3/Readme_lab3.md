# **Лабораторна робота 3**

### Виконала команда № 6
- Ковба Борис, ІА-04
- Новіков Євгеній, ІА-04
- Кучеренко Уляна, ІО-05
- Гуцуляк Наталя, ІО-05
- Дудчик Дмитро, ІО-01
- Співачук Роман, ІО-01
- Павлик Олександр, ІО-04
- Перепелиця Владислав, ІА-04

![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/0e1c9635-244d-4867-a42e-444796baa220)
Swagger API для POST-запитів

![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/13b0fbee-7313-4456-b2d1-bddda7ebb21e)
![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/391bca63-7696-4dfa-9967-09d1f9624c2c)
Перевірка працездатності API для HTTP-ендпойнту

![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/64a6a760-3376-49b4-a1d4-9400407c9a4a)
Повідомлення додалися до БД(BATCH_SIZE було зменшено до 1 для тестування)

![image_2024-03-11_12-28-22](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/3a477f43-8465-41a8-97ef-4c38e4f6cb01)
Відправка повідомлення з використанням протоколу MQTT

![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/7b20964b-01bb-4187-8d26-9b6222669a7f)
Повідомлення побачили клієнти, підписані на потрібний топік

![image](https://github.com/Bulbazavrenok/Techn_IoT/assets/78951357/ae2fc1d7-44a4-4cd5-bfb0-7828611330e1)
Повідомлення, відправлене за допомогою MQTT було додано до БД

Отже, було реалізовано HUB, який дав можливість спілкуватися з БД по двом протоколам: HTTP і MQTT, даючи один спільний інтерфейс для такої комунікації. 
Також його задачею є накопичення повідомлень в кеші для оптимізації доступу до бази данних.
