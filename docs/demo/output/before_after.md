# tzdata 2026b -> 2026c: 169 of 400 appointments would silently show the wrong time

Morocco (Africa/Casablanca, Africa/El_Aaiun) moves to permanent +00 on 2026-09-20; Alberta (America/Edmonton) to permanent -06 from 2026-11-01 (as modelled in tzdata).
Column *shows after upgrade* is what the unchanged stored instant displays under 2026c; *after corrections.sql* is the same row after applying the generated file to a copy.

| zone | affected rows | instant shift |
|---|---:|---|
| Africa/Casablanca | 139 | +1h |
| Africa/El_Aaiun | 22 | +1h |
| America/Edmonton | 8 | -1h |

| id | patient | service | zone | booked for (2026b) | shows after upgrade (2026c) | after corrections.sql | instant shift |
|---:|---|---|---|---|---|---|---|
| 2 | Khadija Garcia | eye exam | Africa/Casablanca | 2027-04-13 14:00 | 2027-04-13 13:00 | 2027-04-13 14:00 | +1h |
| 4 | Lucas Smith | physio | Africa/El_Aaiun | 2026-12-04 15:45 | 2026-12-04 14:45 | 2026-12-04 15:45 | +1h |
| 5 | Liam Martin | physio | Africa/Casablanca | 2027-08-01 17:45 | 2027-08-01 16:45 | 2027-08-01 17:45 | +1h |
| 8 | Mehdi Lee | follow-up | Africa/Casablanca | 2026-12-06 11:00 | 2026-12-06 10:00 | 2026-12-06 11:00 | +1h |
| 9 | Amina Martin | eye exam | Africa/Casablanca | 2027-08-26 09:45 | 2027-08-26 08:45 | 2027-08-26 09:45 | +1h |
| 10 | Ayşe Schmidt | eye exam | Africa/El_Aaiun | 2027-08-11 09:45 | 2027-08-11 08:45 | 2027-08-11 09:45 | +1h |
| 15 | Salma Smith | eye exam | Africa/Casablanca | 2026-10-13 17:00 | 2026-10-13 16:00 | 2026-10-13 17:00 | +1h |
| 16 | Hamza Haddad | dental check-up | Africa/Casablanca | 2027-11-20 12:30 | 2027-11-20 11:30 | 2027-11-20 12:30 | +1h |
| 20 | Salma Garcia | eye exam | Africa/Casablanca | 2027-09-16 15:00 | 2027-09-16 14:00 | 2027-09-16 15:00 | +1h |
| 29 | Emma Lee | eye exam | Africa/Casablanca | 2027-04-30 16:15 | 2027-04-30 15:15 | 2027-04-30 16:15 | +1h |
| 30 | Karim Bouzid | follow-up | Africa/Casablanca | 2027-08-29 17:30 | 2027-08-29 16:30 | 2027-08-29 17:30 | +1h |
| 32 | Mia Kim | eye exam | Africa/Casablanca | 2026-09-27 16:00 | 2026-09-27 15:00 | 2026-09-27 16:00 | +1h |
| 37 | Léa Idrissi | consultation | Africa/El_Aaiun | 2027-08-10 09:00 | 2027-08-10 08:00 | 2027-08-10 09:00 | +1h |
| 38 | Youssef Smith | vaccination | Africa/Casablanca | 2027-05-05 10:00 | 2027-05-05 09:00 | 2027-05-05 10:00 | +1h |
| 43 | Jin Idrissi | vaccination | America/Edmonton | 2027-11-12 16:30 | 2027-11-12 17:30 | 2027-11-12 16:30 | -1h |
| 45 | Jin Haddad | consultation | Africa/Casablanca | 2027-06-13 08:15 | 2027-06-13 07:15 | 2027-06-13 08:15 | +1h |
| 48 | Nadia Schmidt | vaccination | Africa/Casablanca | 2027-10-03 11:30 | 2027-10-03 10:30 | 2027-10-03 11:30 | +1h |
| 49 | Omar Smith | physio | Africa/Casablanca | 2027-10-06 09:00 | 2027-10-06 08:00 | 2027-10-06 09:00 | +1h |
| 50 | Jin Garcia | dental check-up | America/Edmonton | 2027-11-27 16:30 | 2027-11-27 17:30 | 2027-11-27 16:30 | -1h |
| 52 | Mia Haddad | follow-up | Africa/Casablanca | 2027-01-26 08:30 | 2027-01-26 07:30 | 2027-01-26 08:30 | +1h |
| 56 | Karim Bouzid | vaccination | Africa/Casablanca | 2026-11-12 11:15 | 2026-11-12 10:15 | 2026-11-12 11:15 | +1h |
| 57 | Amina Martin | eye exam | Africa/Casablanca | 2026-11-17 14:30 | 2026-11-17 13:30 | 2026-11-17 14:30 | +1h |
| 58 | Youssef Smith | physio | America/Edmonton | 2026-11-17 17:00 | 2026-11-17 18:00 | 2026-11-17 17:00 | -1h |
| 62 | Mia Brown | eye exam | Africa/Casablanca | 2027-10-12 16:30 | 2027-10-12 15:30 | 2027-10-12 16:30 | +1h |
| 64 | Mehdi Alaoui | dental check-up | Africa/Casablanca | 2027-05-02 11:30 | 2027-05-02 10:30 | 2027-05-02 11:30 | +1h |
| 65 | Khadija Martin | physio | Africa/Casablanca | 2027-04-06 08:30 | 2027-04-06 07:30 | 2027-04-06 08:30 | +1h |
| 66 | Khadija Tazi | vaccination | Africa/Casablanca | 2027-05-28 16:15 | 2027-05-28 15:15 | 2027-05-28 16:15 | +1h |
| 67 | Nadia Bouzid | consultation | Africa/Casablanca | 2026-12-25 15:45 | 2026-12-25 14:45 | 2026-12-25 15:45 | +1h |
| 72 | Karim Schmidt | follow-up | Africa/Casablanca | 2027-07-13 11:00 | 2027-07-13 10:00 | 2027-07-13 11:00 | +1h |
| 74 | Liam Lee | physio | Africa/Casablanca | 2027-12-16 14:15 | 2027-12-16 13:15 | 2027-12-16 14:15 | +1h |
| 75 | Noah Alaoui | vaccination | Africa/El_Aaiun | 2026-12-28 17:30 | 2026-12-28 16:30 | 2026-12-28 17:30 | +1h |
| 76 | Fatima El Amrani | follow-up | America/Edmonton | 2027-11-11 09:30 | 2027-11-11 10:30 | 2027-11-11 09:30 | -1h |
| 77 | Omar Idrissi | eye exam | Africa/El_Aaiun | 2026-10-05 14:45 | 2026-10-05 13:45 | 2026-10-05 14:45 | +1h |
| 81 | Lucas El Amrani | physio | Africa/Casablanca | 2026-10-18 10:15 | 2026-10-18 09:15 | 2026-10-18 10:15 | +1h |
| 83 | Omar Tazi | dental check-up | Africa/Casablanca | 2027-01-17 17:15 | 2027-01-17 16:15 | 2027-01-17 17:15 | +1h |
| 86 | Léa Smith | consultation | Africa/Casablanca | 2027-09-05 11:15 | 2027-09-05 10:15 | 2027-09-05 11:15 | +1h |
| 87 | Sophie Alaoui | vaccination | Africa/Casablanca | 2026-12-24 12:15 | 2026-12-24 11:15 | 2026-12-24 12:15 | +1h |
| 92 | Hamza Schmidt | physio | Africa/Casablanca | 2027-06-03 09:00 | 2027-06-03 08:00 | 2027-06-03 09:00 | +1h |
| 96 | Salma Smith | follow-up | Africa/El_Aaiun | 2026-12-03 11:15 | 2026-12-03 10:15 | 2026-12-03 11:15 | +1h |
| 100 | Salma Garcia | eye exam | Africa/Casablanca | 2027-05-17 10:15 | 2027-05-17 09:15 | 2027-05-17 10:15 | +1h |
| 103 | Ayşe Bouzid | vaccination | Africa/Casablanca | 2027-09-16 09:15 | 2027-09-16 08:15 | 2027-09-16 09:15 | +1h |
| 104 | Karim Idrissi | eye exam | Africa/Casablanca | 2027-10-13 12:30 | 2027-10-13 11:30 | 2027-10-13 12:30 | +1h |
| 106 | Jin Schmidt | consultation | Africa/El_Aaiun | 2027-05-04 14:45 | 2027-05-04 13:45 | 2027-05-04 14:45 | +1h |
| 108 | Mia Garcia | physio | Africa/Casablanca | 2026-09-20 12:45 | 2026-09-20 11:45 | 2026-09-20 12:45 | +1h |
| 109 | Omar Benali | eye exam | Africa/Casablanca | 2027-09-13 08:45 | 2027-09-13 07:45 | 2027-09-13 08:45 | +1h |
| 110 | Léa Müller | dental check-up | Africa/El_Aaiun | 2027-04-14 14:00 | 2027-04-14 13:00 | 2027-04-14 14:00 | +1h |
| 113 | Emma Bouzid | vaccination | Africa/Casablanca | 2027-10-01 09:45 | 2027-10-01 08:45 | 2027-10-01 09:45 | +1h |
| 115 | Youssef Bouzid | vaccination | Africa/Casablanca | 2027-07-29 15:45 | 2027-07-29 14:45 | 2027-07-29 15:45 | +1h |
| 116 | Léa Schmidt | dental check-up | Africa/El_Aaiun | 2026-12-10 09:15 | 2026-12-10 08:15 | 2026-12-10 09:15 | +1h |
| 117 | Sophie Benali | eye exam | Africa/Casablanca | 2027-09-08 14:45 | 2027-09-08 13:45 | 2027-09-08 14:45 | +1h |
| 120 | Lucas Tazi | dental check-up | Africa/Casablanca | 2026-11-07 11:45 | 2026-11-07 10:45 | 2026-11-07 11:45 | +1h |
| 125 | Jin Brown | follow-up | Africa/Casablanca | 2027-08-27 12:45 | 2027-08-27 11:45 | 2027-08-27 12:45 | +1h |
| 127 | Mehdi Schmidt | consultation | Africa/Casablanca | 2027-08-14 16:00 | 2027-08-14 15:00 | 2027-08-14 16:00 | +1h |
| 129 | Sophie Müller | physio | Africa/Casablanca | 2027-11-06 10:15 | 2027-11-06 09:15 | 2027-11-06 10:15 | +1h |
| 132 | Karim Martin | physio | America/Edmonton | 2027-03-12 12:15 | 2027-03-12 13:15 | 2027-03-12 12:15 | -1h |
| 133 | Emma Idrissi | follow-up | Africa/Casablanca | 2027-05-10 14:45 | 2027-05-10 13:45 | 2027-05-10 14:45 | +1h |
| 135 | Ahmed Garcia | vaccination | Africa/Casablanca | 2027-12-12 16:30 | 2027-12-12 15:30 | 2027-12-12 16:30 | +1h |
| 136 | Hamza Lee | consultation | Africa/Casablanca | 2026-09-21 10:45 | 2026-09-21 09:45 | 2026-09-21 10:45 | +1h |
| 139 | Omar Haddad | physio | Africa/Casablanca | 2027-02-01 08:00 | 2027-02-01 07:00 | 2027-02-01 08:00 | +1h |
| 142 | Liam Lee | consultation | Africa/Casablanca | 2026-11-26 10:15 | 2026-11-26 09:15 | 2026-11-26 10:15 | +1h |
| 147 | Lucas Martin | consultation | Africa/Casablanca | 2026-10-19 11:45 | 2026-10-19 10:45 | 2026-10-19 11:45 | +1h |
| 148 | Sophie Tazi | follow-up | Africa/Casablanca | 2027-01-03 16:45 | 2027-01-03 15:45 | 2027-01-03 16:45 | +1h |
| 150 | Nadia El Amrani | vaccination | Africa/Casablanca | 2027-08-21 12:00 | 2027-08-21 11:00 | 2027-08-21 12:00 | +1h |
| 151 | Sophie Garcia | follow-up | Africa/Casablanca | 2027-05-30 08:00 | 2027-05-30 07:00 | 2027-05-30 08:00 | +1h |
| 153 | Karim Martin | follow-up | Africa/Casablanca | 2026-12-08 10:30 | 2026-12-08 09:30 | 2026-12-08 10:30 | +1h |
| 154 | Liam Tazi | physio | Africa/Casablanca | 2026-09-29 17:15 | 2026-09-29 16:15 | 2026-09-29 17:15 | +1h |
| 156 | Emma Müller | dental check-up | Africa/Casablanca | 2027-07-02 17:00 | 2027-07-02 16:00 | 2027-07-02 17:00 | +1h |
| 157 | Ayşe Schmidt | dental check-up | Africa/Casablanca | 2026-12-20 10:00 | 2026-12-20 09:00 | 2026-12-20 10:00 | +1h |
| 158 | Khadija Lee | follow-up | Africa/Casablanca | 2027-11-21 09:15 | 2027-11-21 08:15 | 2027-11-21 09:15 | +1h |
| 162 | Hamza El Amrani | consultation | Africa/Casablanca | 2027-08-09 17:00 | 2027-08-09 16:00 | 2027-08-09 17:00 | +1h |
| 163 | Jin Haddad | physio | Africa/Casablanca | 2027-05-28 12:15 | 2027-05-28 11:15 | 2027-05-28 12:15 | +1h |
| 164 | Mia Alaoui | dental check-up | Africa/El_Aaiun | 2027-09-01 16:45 | 2027-09-01 15:45 | 2027-09-01 16:45 | +1h |
| 166 | Mehdi Smith | vaccination | Africa/Casablanca | 2027-11-30 17:15 | 2027-11-30 16:15 | 2027-11-30 17:15 | +1h |
| 168 | Emma Brown | consultation | Africa/Casablanca | 2027-11-03 16:30 | 2027-11-03 15:30 | 2027-11-03 16:30 | +1h |
| 171 | Khadija Schmidt | follow-up | Africa/Casablanca | 2027-03-27 11:30 | 2027-03-27 10:30 | 2027-03-27 11:30 | +1h |
| 173 | Lucas Benali | dental check-up | Africa/Casablanca | 2026-10-08 14:15 | 2026-10-08 13:15 | 2026-10-08 14:15 | +1h |
| 174 | Mehdi Martin | physio | Africa/Casablanca | 2026-09-21 17:15 | 2026-09-21 16:15 | 2026-09-21 17:15 | +1h |
| 176 | Nadia Benali | follow-up | Africa/Casablanca | 2027-11-25 17:30 | 2027-11-25 16:30 | 2027-11-25 17:30 | +1h |
| 177 | Léa Brown | dental check-up | Africa/Casablanca | 2027-01-22 08:45 | 2027-01-22 07:45 | 2027-01-22 08:45 | +1h |
| 179 | Youssef Kim | physio | Africa/El_Aaiun | 2027-05-17 08:00 | 2027-05-17 07:00 | 2027-05-17 08:00 | +1h |
| 181 | Lucas Idrissi | follow-up | Africa/El_Aaiun | 2026-10-30 10:30 | 2026-10-30 09:30 | 2026-10-30 10:30 | +1h |
| 183 | Fatima Alaoui | dental check-up | Africa/Casablanca | 2027-01-04 10:00 | 2027-01-04 09:00 | 2027-01-04 10:00 | +1h |
| 187 | Mia Idrissi | eye exam | Africa/Casablanca | 2027-03-15 15:45 | 2027-03-15 14:45 | 2027-03-15 15:45 | +1h |
| 188 | Noah Kim | vaccination | America/Edmonton | 2027-01-11 17:30 | 2027-01-11 18:30 | 2027-01-11 17:30 | -1h |
| 189 | Lucas Idrissi | consultation | Africa/Casablanca | 2027-12-21 12:15 | 2027-12-21 11:15 | 2027-12-21 12:15 | +1h |
| 190 | Nadia Lee | dental check-up | Africa/Casablanca | 2027-12-21 17:45 | 2027-12-21 16:45 | 2027-12-21 17:45 | +1h |
| 191 | Jin Müller | eye exam | Africa/Casablanca | 2027-10-02 14:45 | 2027-10-02 13:45 | 2027-10-02 14:45 | +1h |
| 192 | Emma El Amrani | vaccination | Africa/Casablanca | 2027-01-29 16:30 | 2027-01-29 15:30 | 2027-01-29 16:30 | +1h |
| 193 | Mehdi Idrissi | vaccination | Africa/Casablanca | 2026-10-17 15:30 | 2026-10-17 14:30 | 2026-10-17 15:30 | +1h |
| 196 | Ahmed Garcia | consultation | Africa/Casablanca | 2027-01-25 11:15 | 2027-01-25 10:15 | 2027-01-25 11:15 | +1h |
| 199 | Nadia Brown | follow-up | Africa/Casablanca | 2026-10-30 14:00 | 2026-10-30 13:00 | 2026-10-30 14:00 | +1h |
| 201 | Hamza Haddad | dental check-up | Africa/Casablanca | 2026-12-18 15:00 | 2026-12-18 14:00 | 2026-12-18 15:00 | +1h |
| 203 | Mehdi Martin | dental check-up | Africa/Casablanca | 2027-01-12 15:00 | 2027-01-12 14:00 | 2027-01-12 15:00 | +1h |
| 207 | Mia Benali | eye exam | Africa/Casablanca | 2027-10-06 08:15 | 2027-10-06 07:15 | 2027-10-06 08:15 | +1h |
| 216 | Ahmed Smith | vaccination | Africa/Casablanca | 2026-11-08 14:45 | 2026-11-08 13:45 | 2026-11-08 14:45 | +1h |
| 217 | Jin Smith | consultation | Africa/El_Aaiun | 2026-11-30 12:30 | 2026-11-30 11:30 | 2026-11-30 12:30 | +1h |
| 218 | Mia Müller | dental check-up | Africa/Casablanca | 2027-06-21 12:45 | 2027-06-21 11:45 | 2027-06-21 12:45 | +1h |
| 219 | Mia Brown | consultation | Africa/Casablanca | 2026-11-02 10:00 | 2026-11-02 09:00 | 2026-11-02 10:00 | +1h |
| 220 | Mehdi Bouzid | dental check-up | Africa/Casablanca | 2026-10-06 14:45 | 2026-10-06 13:45 | 2026-10-06 14:45 | +1h |
| 221 | Youssef Müller | vaccination | Africa/El_Aaiun | 2026-11-03 16:00 | 2026-11-03 15:00 | 2026-11-03 16:00 | +1h |
| 224 | Amina Martin | dental check-up | Africa/Casablanca | 2027-10-13 08:15 | 2027-10-13 07:15 | 2027-10-13 08:15 | +1h |
| 225 | Noah Tazi | vaccination | Africa/Casablanca | 2027-12-01 08:00 | 2027-12-01 07:00 | 2027-12-01 08:00 | +1h |
| 227 | Fatima Kim | vaccination | Africa/Casablanca | 2027-10-23 16:00 | 2027-10-23 15:00 | 2027-10-23 16:00 | +1h |
| 229 | Ahmed Idrissi | consultation | Africa/Casablanca | 2027-03-15 16:15 | 2027-03-15 15:15 | 2027-03-15 16:15 | +1h |
| 233 | Nadia Alaoui | physio | Africa/Casablanca | 2027-07-11 10:30 | 2027-07-11 09:30 | 2027-07-11 10:30 | +1h |
| 236 | Fatima El Amrani | vaccination | Africa/Casablanca | 2027-07-07 08:15 | 2027-07-07 07:15 | 2027-07-07 08:15 | +1h |
| 238 | Karim Martin | eye exam | Africa/Casablanca | 2027-10-03 11:45 | 2027-10-03 10:45 | 2027-10-03 11:45 | +1h |
| 241 | Liam Smith | vaccination | Africa/Casablanca | 2027-05-06 12:15 | 2027-05-06 11:15 | 2027-05-06 12:15 | +1h |
| 244 | Karim Schmidt | follow-up | Africa/Casablanca | 2027-07-21 16:00 | 2027-07-21 15:00 | 2027-07-21 16:00 | +1h |
| 249 | Mehdi Martin | physio | Africa/Casablanca | 2026-11-29 12:00 | 2026-11-29 11:00 | 2026-11-29 12:00 | +1h |
| 251 | Noah Müller | dental check-up | Africa/Casablanca | 2027-01-27 16:15 | 2027-01-27 15:15 | 2027-01-27 16:15 | +1h |
| 253 | Lucas Brown | consultation | Africa/Casablanca | 2027-05-26 11:00 | 2027-05-26 10:00 | 2027-05-26 11:00 | +1h |
| 255 | Salma Idrissi | physio | Africa/Casablanca | 2026-12-18 11:45 | 2026-12-18 10:45 | 2026-12-18 11:45 | +1h |
| 256 | Jin Smith | physio | Africa/Casablanca | 2027-12-19 10:45 | 2027-12-19 09:45 | 2027-12-19 10:45 | +1h |
| 260 | Sophie Smith | vaccination | Africa/Casablanca | 2026-11-23 15:00 | 2026-11-23 14:00 | 2026-11-23 15:00 | +1h |
| 266 | Mehdi Smith | follow-up | Africa/Casablanca | 2026-10-30 10:00 | 2026-10-30 09:00 | 2026-10-30 10:00 | +1h |
| 267 | Salma Idrissi | follow-up | Africa/Casablanca | 2027-06-16 11:45 | 2027-06-16 10:45 | 2027-06-16 11:45 | +1h |
| 268 | Emma El Amrani | follow-up | Africa/Casablanca | 2027-05-30 15:45 | 2027-05-30 14:45 | 2027-05-30 15:45 | +1h |
| 269 | Lucas Bouzid | dental check-up | America/Edmonton | 2027-01-16 15:15 | 2027-01-16 16:15 | 2027-01-16 15:15 | -1h |
| 270 | Youssef Martin | eye exam | Africa/Casablanca | 2027-06-13 10:45 | 2027-06-13 09:45 | 2027-06-13 10:45 | +1h |
| 274 | Jin El Amrani | dental check-up | Africa/Casablanca | 2026-12-26 17:00 | 2026-12-26 16:00 | 2026-12-26 17:00 | +1h |
| 276 | Léa Tazi | eye exam | Africa/Casablanca | 2027-10-13 08:30 | 2027-10-13 07:30 | 2027-10-13 08:30 | +1h |
| 278 | Léa Tazi | consultation | Africa/Casablanca | 2027-01-05 17:00 | 2027-01-05 16:00 | 2027-01-05 17:00 | +1h |
| 281 | Khadija Martin | consultation | Africa/Casablanca | 2027-03-26 15:30 | 2027-03-26 14:30 | 2027-03-26 15:30 | +1h |
| 283 | Salma Schmidt | physio | Africa/Casablanca | 2027-10-19 14:15 | 2027-10-19 13:15 | 2027-10-19 14:15 | +1h |
| 286 | Noah Garcia | eye exam | Africa/Casablanca | 2027-11-06 08:45 | 2027-11-06 07:45 | 2027-11-06 08:45 | +1h |
| 288 | Karim Smith | physio | Africa/Casablanca | 2026-11-02 08:30 | 2026-11-02 07:30 | 2026-11-02 08:30 | +1h |
| 290 | Salma Bouzid | dental check-up | Africa/Casablanca | 2027-01-26 11:30 | 2027-01-26 10:30 | 2027-01-26 11:30 | +1h |
| 296 | Mehdi Lee | eye exam | Africa/El_Aaiun | 2027-10-13 16:00 | 2027-10-13 15:00 | 2027-10-13 16:00 | +1h |
| 297 | Mia Müller | dental check-up | Africa/Casablanca | 2027-10-30 17:00 | 2027-10-30 16:00 | 2027-10-30 17:00 | +1h |
| 301 | Lucas Bouzid | physio | Africa/Casablanca | 2026-10-31 15:15 | 2026-10-31 14:15 | 2026-10-31 15:15 | +1h |
| 303 | Ayşe El Amrani | dental check-up | Africa/Casablanca | 2027-11-23 15:00 | 2027-11-23 14:00 | 2027-11-23 15:00 | +1h |
| 308 | Khadija Schmidt | consultation | Africa/Casablanca | 2027-12-13 10:45 | 2027-12-13 09:45 | 2027-12-13 10:45 | +1h |
| 314 | Hamza Tazi | eye exam | Africa/Casablanca | 2027-08-17 12:30 | 2027-08-17 11:30 | 2027-08-17 12:30 | +1h |
| 316 | Jin Müller | eye exam | Africa/El_Aaiun | 2027-01-15 10:00 | 2027-01-15 09:00 | 2027-01-15 10:00 | +1h |
| 322 | Jin Bouzid | consultation | Africa/Casablanca | 2026-12-15 10:00 | 2026-12-15 09:00 | 2026-12-15 10:00 | +1h |
| 323 | Hamza Müller | follow-up | Africa/El_Aaiun | 2026-12-11 09:45 | 2026-12-11 08:45 | 2026-12-11 09:45 | +1h |
| 324 | Youssef Müller | vaccination | Africa/Casablanca | 2027-11-10 12:45 | 2027-11-10 11:45 | 2027-11-10 12:45 | +1h |
| 327 | Sophie Schmidt | eye exam | Africa/Casablanca | 2027-05-19 16:30 | 2027-05-19 15:30 | 2027-05-19 16:30 | +1h |
| 329 | Noah Garcia | follow-up | Africa/Casablanca | 2027-03-19 17:00 | 2027-03-19 16:00 | 2027-03-19 17:00 | +1h |
| 332 | Liam Schmidt | dental check-up | Africa/Casablanca | 2027-12-08 11:15 | 2027-12-08 10:15 | 2027-12-08 11:15 | +1h |
| 333 | Omar Idrissi | dental check-up | Africa/El_Aaiun | 2027-05-08 16:15 | 2027-05-08 15:15 | 2027-05-08 16:15 | +1h |
| 339 | Amina Müller | vaccination | Africa/Casablanca | 2027-11-28 09:30 | 2027-11-28 08:30 | 2027-11-28 09:30 | +1h |
| 341 | Nadia Bouzid | eye exam | Africa/Casablanca | 2027-10-30 14:00 | 2027-10-30 13:00 | 2027-10-30 14:00 | +1h |
| 342 | Youssef Benali | follow-up | Africa/Casablanca | 2027-05-07 08:15 | 2027-05-07 07:15 | 2027-05-07 08:15 | +1h |
| 343 | Khadija Schmidt | follow-up | Africa/Casablanca | 2026-10-21 12:15 | 2026-10-21 11:15 | 2026-10-21 12:15 | +1h |
| 345 | Lucas Alaoui | consultation | Africa/El_Aaiun | 2027-05-10 14:00 | 2027-05-10 13:00 | 2027-05-10 14:00 | +1h |
| 347 | Mia Brown | consultation | Africa/Casablanca | 2027-06-28 14:00 | 2027-06-28 13:00 | 2027-06-28 14:00 | +1h |
| 351 | Léa Garcia | consultation | Africa/Casablanca | 2027-09-21 12:00 | 2027-09-21 11:00 | 2027-09-21 12:00 | +1h |
| 353 | Omar Schmidt | vaccination | Africa/Casablanca | 2027-12-03 10:00 | 2027-12-03 09:00 | 2027-12-03 10:00 | +1h |
| 356 | Khadija Idrissi | vaccination | Africa/El_Aaiun | 2026-10-28 17:00 | 2026-10-28 16:00 | 2026-10-28 17:00 | +1h |
| 357 | Ahmed Kim | vaccination | Africa/Casablanca | 2026-12-04 15:30 | 2026-12-04 14:30 | 2026-12-04 15:30 | +1h |
| 360 | Hamza Alaoui | consultation | Africa/El_Aaiun | 2027-03-31 16:00 | 2027-03-31 15:00 | 2027-03-31 16:00 | +1h |
| 364 | Ahmed Smith | follow-up | Africa/Casablanca | 2026-11-08 16:15 | 2026-11-08 15:15 | 2026-11-08 16:15 | +1h |
| 369 | Mia El Amrani | vaccination | Africa/El_Aaiun | 2027-11-02 10:15 | 2027-11-02 09:15 | 2027-11-02 10:15 | +1h |
| 370 | Karim Benali | consultation | Africa/Casablanca | 2026-11-15 12:15 | 2026-11-15 11:15 | 2026-11-15 12:15 | +1h |
| 371 | Ayşe El Amrani | physio | Africa/Casablanca | 2026-12-03 10:30 | 2026-12-03 09:30 | 2026-12-03 10:30 | +1h |
| 372 | Karim Müller | physio | Africa/Casablanca | 2027-04-19 10:15 | 2027-04-19 09:15 | 2027-04-19 10:15 | +1h |
| 373 | Lucas Müller | vaccination | Africa/Casablanca | 2026-12-19 15:45 | 2026-12-19 14:45 | 2026-12-19 15:45 | +1h |
| 375 | Emma Müller | eye exam | Africa/Casablanca | 2027-09-16 16:30 | 2027-09-16 15:30 | 2027-09-16 16:30 | +1h |
| 377 | Amina Haddad | physio | Africa/Casablanca | 2027-12-08 12:30 | 2027-12-08 11:30 | 2027-12-08 12:30 | +1h |
| 378 | Mia Kim | vaccination | Africa/Casablanca | 2027-07-28 10:15 | 2027-07-28 09:15 | 2027-07-28 10:15 | +1h |
| 379 | Lucas Garcia | physio | Africa/Casablanca | 2027-05-07 09:45 | 2027-05-07 08:45 | 2027-05-07 09:45 | +1h |
| 380 | Mehdi Smith | physio | Africa/Casablanca | 2026-12-27 11:15 | 2026-12-27 10:15 | 2026-12-27 11:15 | +1h |
| 381 | Noah Alaoui | vaccination | America/Edmonton | 2027-12-14 12:00 | 2027-12-14 13:00 | 2027-12-14 12:00 | -1h |
| 385 | Mia El Amrani | physio | Africa/Casablanca | 2027-12-19 15:15 | 2027-12-19 14:15 | 2027-12-19 15:15 | +1h |
| 393 | Omar Tazi | consultation | Africa/Casablanca | 2027-12-24 10:00 | 2027-12-24 09:00 | 2027-12-24 10:00 | +1h |
| 396 | Youssef Bouzid | follow-up | Africa/Casablanca | 2026-11-05 10:30 | 2026-11-05 09:30 | 2026-11-05 10:30 | +1h |
| 400 | Mia Kim | vaccination | Africa/Casablanca | 2027-06-10 08:15 | 2027-06-10 07:15 | 2027-06-10 08:15 | +1h |
