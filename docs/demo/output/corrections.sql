-- tzimpact corrections: 2026b -> 2026c
-- table "appointments"  instant column "starts_at"  zone column "tz"  id column "id"
-- generated 2026-09-06T15:05:27Z by tzimpact 0.0.1. REVIEW BEFORE APPLYING. tzimpact never executes this file.
-- semantics: wall-clock (each row keeps the local time it was booked for; the stored instant moves)
-- Every UPDATE matches only a row still holding its pre-correction value, so applying this file twice changes nothing.
-- ONE-SHOT: run `tzimpact scan` once per release upgrade. After applying this file do NOT scan and regenerate:
-- corrected instants still lie inside the change windows and a regenerated file would move them again.
-- corrections: 169 rows  |  manual review: 0
BEGIN;
-- Africa/Casablanca  row 2  intended 2027-04-13 14:00  currently shows 2027-04-13 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-04-13T14:00:00Z' WHERE "id" = 2 AND "starts_at" = '2027-04-13T13:00:00Z';
-- Africa/Casablanca  row 5  intended 2027-08-01 17:45  currently shows 2027-08-01 16:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-01T17:45:00Z' WHERE "id" = 5 AND "starts_at" = '2027-08-01T16:45:00Z';
-- Africa/Casablanca  row 8  intended 2026-12-06 11:00  currently shows 2026-12-06 10:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-06T11:00:00Z' WHERE "id" = 8 AND "starts_at" = '2026-12-06T10:00:00Z';
-- Africa/Casablanca  row 9  intended 2027-08-26 09:45  currently shows 2027-08-26 08:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-26T09:45:00Z' WHERE "id" = 9 AND "starts_at" = '2027-08-26T08:45:00Z';
-- Africa/Casablanca  row 15  intended 2026-10-13 17:00  currently shows 2026-10-13 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-13T17:00:00Z' WHERE "id" = 15 AND "starts_at" = '2026-10-13T16:00:00Z';
-- Africa/Casablanca  row 16  intended 2027-11-20 12:30  currently shows 2027-11-20 11:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-20T12:30:00Z' WHERE "id" = 16 AND "starts_at" = '2027-11-20T11:30:00Z';
-- Africa/Casablanca  row 20  intended 2027-09-16 15:00  currently shows 2027-09-16 14:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-16T15:00:00Z' WHERE "id" = 20 AND "starts_at" = '2027-09-16T14:00:00Z';
-- Africa/Casablanca  row 29  intended 2027-04-30 16:15  currently shows 2027-04-30 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-04-30T16:15:00Z' WHERE "id" = 29 AND "starts_at" = '2027-04-30T15:15:00Z';
-- Africa/Casablanca  row 30  intended 2027-08-29 17:30  currently shows 2027-08-29 16:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-29T17:30:00Z' WHERE "id" = 30 AND "starts_at" = '2027-08-29T16:30:00Z';
-- Africa/Casablanca  row 32  intended 2026-09-27 16:00  currently shows 2026-09-27 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-09-27T16:00:00Z' WHERE "id" = 32 AND "starts_at" = '2026-09-27T15:00:00Z';
-- Africa/Casablanca  row 38  intended 2027-05-05 10:00  currently shows 2027-05-05 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-05T10:00:00Z' WHERE "id" = 38 AND "starts_at" = '2027-05-05T09:00:00Z';
-- Africa/Casablanca  row 45  intended 2027-06-13 08:15  currently shows 2027-06-13 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-13T08:15:00Z' WHERE "id" = 45 AND "starts_at" = '2027-06-13T07:15:00Z';
-- Africa/Casablanca  row 48  intended 2027-10-03 11:30  currently shows 2027-10-03 10:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-03T11:30:00Z' WHERE "id" = 48 AND "starts_at" = '2027-10-03T10:30:00Z';
-- Africa/Casablanca  row 49  intended 2027-10-06 09:00  currently shows 2027-10-06 08:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-06T09:00:00Z' WHERE "id" = 49 AND "starts_at" = '2027-10-06T08:00:00Z';
-- Africa/Casablanca  row 52  intended 2027-01-26 08:30  currently shows 2027-01-26 07:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-26T08:30:00Z' WHERE "id" = 52 AND "starts_at" = '2027-01-26T07:30:00Z';
-- Africa/Casablanca  row 56  intended 2026-11-12 11:15  currently shows 2026-11-12 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-12T11:15:00Z' WHERE "id" = 56 AND "starts_at" = '2026-11-12T10:15:00Z';
-- Africa/Casablanca  row 57  intended 2026-11-17 14:30  currently shows 2026-11-17 13:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-17T14:30:00Z' WHERE "id" = 57 AND "starts_at" = '2026-11-17T13:30:00Z';
-- Africa/Casablanca  row 62  intended 2027-10-12 16:30  currently shows 2027-10-12 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-12T16:30:00Z' WHERE "id" = 62 AND "starts_at" = '2027-10-12T15:30:00Z';
-- Africa/Casablanca  row 64  intended 2027-05-02 11:30  currently shows 2027-05-02 10:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-02T11:30:00Z' WHERE "id" = 64 AND "starts_at" = '2027-05-02T10:30:00Z';
-- Africa/Casablanca  row 65  intended 2027-04-06 08:30  currently shows 2027-04-06 07:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-04-06T08:30:00Z' WHERE "id" = 65 AND "starts_at" = '2027-04-06T07:30:00Z';
-- Africa/Casablanca  row 66  intended 2027-05-28 16:15  currently shows 2027-05-28 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-28T16:15:00Z' WHERE "id" = 66 AND "starts_at" = '2027-05-28T15:15:00Z';
-- Africa/Casablanca  row 67  intended 2026-12-25 15:45  currently shows 2026-12-25 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-25T15:45:00Z' WHERE "id" = 67 AND "starts_at" = '2026-12-25T14:45:00Z';
-- Africa/Casablanca  row 72  intended 2027-07-13 11:00  currently shows 2027-07-13 10:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-13T11:00:00Z' WHERE "id" = 72 AND "starts_at" = '2027-07-13T10:00:00Z';
-- Africa/Casablanca  row 74  intended 2027-12-16 14:15  currently shows 2027-12-16 13:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-16T14:15:00Z' WHERE "id" = 74 AND "starts_at" = '2027-12-16T13:15:00Z';
-- Africa/Casablanca  row 81  intended 2026-10-18 10:15  currently shows 2026-10-18 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-18T10:15:00Z' WHERE "id" = 81 AND "starts_at" = '2026-10-18T09:15:00Z';
-- Africa/Casablanca  row 83  intended 2027-01-17 17:15  currently shows 2027-01-17 16:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-17T17:15:00Z' WHERE "id" = 83 AND "starts_at" = '2027-01-17T16:15:00Z';
-- Africa/Casablanca  row 86  intended 2027-09-05 11:15  currently shows 2027-09-05 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-05T11:15:00Z' WHERE "id" = 86 AND "starts_at" = '2027-09-05T10:15:00Z';
-- Africa/Casablanca  row 87  intended 2026-12-24 12:15  currently shows 2026-12-24 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-24T12:15:00Z' WHERE "id" = 87 AND "starts_at" = '2026-12-24T11:15:00Z';
-- Africa/Casablanca  row 92  intended 2027-06-03 09:00  currently shows 2027-06-03 08:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-03T09:00:00Z' WHERE "id" = 92 AND "starts_at" = '2027-06-03T08:00:00Z';
-- Africa/Casablanca  row 100  intended 2027-05-17 10:15  currently shows 2027-05-17 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-17T10:15:00Z' WHERE "id" = 100 AND "starts_at" = '2027-05-17T09:15:00Z';
-- Africa/Casablanca  row 103  intended 2027-09-16 09:15  currently shows 2027-09-16 08:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-16T09:15:00Z' WHERE "id" = 103 AND "starts_at" = '2027-09-16T08:15:00Z';
-- Africa/Casablanca  row 104  intended 2027-10-13 12:30  currently shows 2027-10-13 11:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-13T12:30:00Z' WHERE "id" = 104 AND "starts_at" = '2027-10-13T11:30:00Z';
-- Africa/Casablanca  row 108  intended 2026-09-20 12:45  currently shows 2026-09-20 11:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-09-20T12:45:00Z' WHERE "id" = 108 AND "starts_at" = '2026-09-20T11:45:00Z';
-- Africa/Casablanca  row 109  intended 2027-09-13 08:45  currently shows 2027-09-13 07:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-13T08:45:00Z' WHERE "id" = 109 AND "starts_at" = '2027-09-13T07:45:00Z';
-- Africa/Casablanca  row 113  intended 2027-10-01 09:45  currently shows 2027-10-01 08:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-01T09:45:00Z' WHERE "id" = 113 AND "starts_at" = '2027-10-01T08:45:00Z';
-- Africa/Casablanca  row 115  intended 2027-07-29 15:45  currently shows 2027-07-29 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-29T15:45:00Z' WHERE "id" = 115 AND "starts_at" = '2027-07-29T14:45:00Z';
-- Africa/Casablanca  row 117  intended 2027-09-08 14:45  currently shows 2027-09-08 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-08T14:45:00Z' WHERE "id" = 117 AND "starts_at" = '2027-09-08T13:45:00Z';
-- Africa/Casablanca  row 120  intended 2026-11-07 11:45  currently shows 2026-11-07 10:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-07T11:45:00Z' WHERE "id" = 120 AND "starts_at" = '2026-11-07T10:45:00Z';
-- Africa/Casablanca  row 125  intended 2027-08-27 12:45  currently shows 2027-08-27 11:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-27T12:45:00Z' WHERE "id" = 125 AND "starts_at" = '2027-08-27T11:45:00Z';
-- Africa/Casablanca  row 127  intended 2027-08-14 16:00  currently shows 2027-08-14 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-14T16:00:00Z' WHERE "id" = 127 AND "starts_at" = '2027-08-14T15:00:00Z';
-- Africa/Casablanca  row 129  intended 2027-11-06 10:15  currently shows 2027-11-06 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-06T10:15:00Z' WHERE "id" = 129 AND "starts_at" = '2027-11-06T09:15:00Z';
-- Africa/Casablanca  row 133  intended 2027-05-10 14:45  currently shows 2027-05-10 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-10T14:45:00Z' WHERE "id" = 133 AND "starts_at" = '2027-05-10T13:45:00Z';
-- Africa/Casablanca  row 135  intended 2027-12-12 16:30  currently shows 2027-12-12 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-12T16:30:00Z' WHERE "id" = 135 AND "starts_at" = '2027-12-12T15:30:00Z';
-- Africa/Casablanca  row 136  intended 2026-09-21 10:45  currently shows 2026-09-21 09:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-09-21T10:45:00Z' WHERE "id" = 136 AND "starts_at" = '2026-09-21T09:45:00Z';
-- Africa/Casablanca  row 139  intended 2027-02-01 08:00  currently shows 2027-02-01 07:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-02-01T08:00:00Z' WHERE "id" = 139 AND "starts_at" = '2027-02-01T07:00:00Z';
-- Africa/Casablanca  row 142  intended 2026-11-26 10:15  currently shows 2026-11-26 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-26T10:15:00Z' WHERE "id" = 142 AND "starts_at" = '2026-11-26T09:15:00Z';
-- Africa/Casablanca  row 147  intended 2026-10-19 11:45  currently shows 2026-10-19 10:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-19T11:45:00Z' WHERE "id" = 147 AND "starts_at" = '2026-10-19T10:45:00Z';
-- Africa/Casablanca  row 148  intended 2027-01-03 16:45  currently shows 2027-01-03 15:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-03T16:45:00Z' WHERE "id" = 148 AND "starts_at" = '2027-01-03T15:45:00Z';
-- Africa/Casablanca  row 150  intended 2027-08-21 12:00  currently shows 2027-08-21 11:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-21T12:00:00Z' WHERE "id" = 150 AND "starts_at" = '2027-08-21T11:00:00Z';
-- Africa/Casablanca  row 151  intended 2027-05-30 08:00  currently shows 2027-05-30 07:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-30T08:00:00Z' WHERE "id" = 151 AND "starts_at" = '2027-05-30T07:00:00Z';
-- Africa/Casablanca  row 153  intended 2026-12-08 10:30  currently shows 2026-12-08 09:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-08T10:30:00Z' WHERE "id" = 153 AND "starts_at" = '2026-12-08T09:30:00Z';
-- Africa/Casablanca  row 154  intended 2026-09-29 17:15  currently shows 2026-09-29 16:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-09-29T17:15:00Z' WHERE "id" = 154 AND "starts_at" = '2026-09-29T16:15:00Z';
-- Africa/Casablanca  row 156  intended 2027-07-02 17:00  currently shows 2027-07-02 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-02T17:00:00Z' WHERE "id" = 156 AND "starts_at" = '2027-07-02T16:00:00Z';
-- Africa/Casablanca  row 157  intended 2026-12-20 10:00  currently shows 2026-12-20 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-20T10:00:00Z' WHERE "id" = 157 AND "starts_at" = '2026-12-20T09:00:00Z';
-- Africa/Casablanca  row 158  intended 2027-11-21 09:15  currently shows 2027-11-21 08:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-21T09:15:00Z' WHERE "id" = 158 AND "starts_at" = '2027-11-21T08:15:00Z';
-- Africa/Casablanca  row 162  intended 2027-08-09 17:00  currently shows 2027-08-09 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-09T17:00:00Z' WHERE "id" = 162 AND "starts_at" = '2027-08-09T16:00:00Z';
-- Africa/Casablanca  row 163  intended 2027-05-28 12:15  currently shows 2027-05-28 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-28T12:15:00Z' WHERE "id" = 163 AND "starts_at" = '2027-05-28T11:15:00Z';
-- Africa/Casablanca  row 166  intended 2027-11-30 17:15  currently shows 2027-11-30 16:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-30T17:15:00Z' WHERE "id" = 166 AND "starts_at" = '2027-11-30T16:15:00Z';
-- Africa/Casablanca  row 168  intended 2027-11-03 16:30  currently shows 2027-11-03 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-03T16:30:00Z' WHERE "id" = 168 AND "starts_at" = '2027-11-03T15:30:00Z';
-- Africa/Casablanca  row 171  intended 2027-03-27 11:30  currently shows 2027-03-27 10:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-27T11:30:00Z' WHERE "id" = 171 AND "starts_at" = '2027-03-27T10:30:00Z';
-- Africa/Casablanca  row 173  intended 2026-10-08 14:15  currently shows 2026-10-08 13:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-08T14:15:00Z' WHERE "id" = 173 AND "starts_at" = '2026-10-08T13:15:00Z';
-- Africa/Casablanca  row 174  intended 2026-09-21 17:15  currently shows 2026-09-21 16:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-09-21T17:15:00Z' WHERE "id" = 174 AND "starts_at" = '2026-09-21T16:15:00Z';
-- Africa/Casablanca  row 176  intended 2027-11-25 17:30  currently shows 2027-11-25 16:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-25T17:30:00Z' WHERE "id" = 176 AND "starts_at" = '2027-11-25T16:30:00Z';
-- Africa/Casablanca  row 177  intended 2027-01-22 08:45  currently shows 2027-01-22 07:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-22T08:45:00Z' WHERE "id" = 177 AND "starts_at" = '2027-01-22T07:45:00Z';
-- Africa/Casablanca  row 183  intended 2027-01-04 10:00  currently shows 2027-01-04 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-04T10:00:00Z' WHERE "id" = 183 AND "starts_at" = '2027-01-04T09:00:00Z';
-- Africa/Casablanca  row 187  intended 2027-03-15 15:45  currently shows 2027-03-15 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-15T15:45:00Z' WHERE "id" = 187 AND "starts_at" = '2027-03-15T14:45:00Z';
-- Africa/Casablanca  row 189  intended 2027-12-21 12:15  currently shows 2027-12-21 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-21T12:15:00Z' WHERE "id" = 189 AND "starts_at" = '2027-12-21T11:15:00Z';
-- Africa/Casablanca  row 190  intended 2027-12-21 17:45  currently shows 2027-12-21 16:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-21T17:45:00Z' WHERE "id" = 190 AND "starts_at" = '2027-12-21T16:45:00Z';
-- Africa/Casablanca  row 191  intended 2027-10-02 14:45  currently shows 2027-10-02 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-02T14:45:00Z' WHERE "id" = 191 AND "starts_at" = '2027-10-02T13:45:00Z';
-- Africa/Casablanca  row 192  intended 2027-01-29 16:30  currently shows 2027-01-29 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-29T16:30:00Z' WHERE "id" = 192 AND "starts_at" = '2027-01-29T15:30:00Z';
-- Africa/Casablanca  row 193  intended 2026-10-17 15:30  currently shows 2026-10-17 14:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-17T15:30:00Z' WHERE "id" = 193 AND "starts_at" = '2026-10-17T14:30:00Z';
-- Africa/Casablanca  row 196  intended 2027-01-25 11:15  currently shows 2027-01-25 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-25T11:15:00Z' WHERE "id" = 196 AND "starts_at" = '2027-01-25T10:15:00Z';
-- Africa/Casablanca  row 199  intended 2026-10-30 14:00  currently shows 2026-10-30 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-30T14:00:00Z' WHERE "id" = 199 AND "starts_at" = '2026-10-30T13:00:00Z';
-- Africa/Casablanca  row 201  intended 2026-12-18 15:00  currently shows 2026-12-18 14:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-18T15:00:00Z' WHERE "id" = 201 AND "starts_at" = '2026-12-18T14:00:00Z';
-- Africa/Casablanca  row 203  intended 2027-01-12 15:00  currently shows 2027-01-12 14:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-12T15:00:00Z' WHERE "id" = 203 AND "starts_at" = '2027-01-12T14:00:00Z';
-- Africa/Casablanca  row 207  intended 2027-10-06 08:15  currently shows 2027-10-06 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-06T08:15:00Z' WHERE "id" = 207 AND "starts_at" = '2027-10-06T07:15:00Z';
-- Africa/Casablanca  row 216  intended 2026-11-08 14:45  currently shows 2026-11-08 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-08T14:45:00Z' WHERE "id" = 216 AND "starts_at" = '2026-11-08T13:45:00Z';
-- Africa/Casablanca  row 218  intended 2027-06-21 12:45  currently shows 2027-06-21 11:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-21T12:45:00Z' WHERE "id" = 218 AND "starts_at" = '2027-06-21T11:45:00Z';
-- Africa/Casablanca  row 219  intended 2026-11-02 10:00  currently shows 2026-11-02 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-02T10:00:00Z' WHERE "id" = 219 AND "starts_at" = '2026-11-02T09:00:00Z';
-- Africa/Casablanca  row 220  intended 2026-10-06 14:45  currently shows 2026-10-06 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-06T14:45:00Z' WHERE "id" = 220 AND "starts_at" = '2026-10-06T13:45:00Z';
-- Africa/Casablanca  row 224  intended 2027-10-13 08:15  currently shows 2027-10-13 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-13T08:15:00Z' WHERE "id" = 224 AND "starts_at" = '2027-10-13T07:15:00Z';
-- Africa/Casablanca  row 225  intended 2027-12-01 08:00  currently shows 2027-12-01 07:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-01T08:00:00Z' WHERE "id" = 225 AND "starts_at" = '2027-12-01T07:00:00Z';
-- Africa/Casablanca  row 227  intended 2027-10-23 16:00  currently shows 2027-10-23 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-23T16:00:00Z' WHERE "id" = 227 AND "starts_at" = '2027-10-23T15:00:00Z';
-- Africa/Casablanca  row 229  intended 2027-03-15 16:15  currently shows 2027-03-15 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-15T16:15:00Z' WHERE "id" = 229 AND "starts_at" = '2027-03-15T15:15:00Z';
-- Africa/Casablanca  row 233  intended 2027-07-11 10:30  currently shows 2027-07-11 09:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-11T10:30:00Z' WHERE "id" = 233 AND "starts_at" = '2027-07-11T09:30:00Z';
-- Africa/Casablanca  row 236  intended 2027-07-07 08:15  currently shows 2027-07-07 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-07T08:15:00Z' WHERE "id" = 236 AND "starts_at" = '2027-07-07T07:15:00Z';
-- Africa/Casablanca  row 238  intended 2027-10-03 11:45  currently shows 2027-10-03 10:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-03T11:45:00Z' WHERE "id" = 238 AND "starts_at" = '2027-10-03T10:45:00Z';
-- Africa/Casablanca  row 241  intended 2027-05-06 12:15  currently shows 2027-05-06 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-06T12:15:00Z' WHERE "id" = 241 AND "starts_at" = '2027-05-06T11:15:00Z';
-- Africa/Casablanca  row 244  intended 2027-07-21 16:00  currently shows 2027-07-21 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-21T16:00:00Z' WHERE "id" = 244 AND "starts_at" = '2027-07-21T15:00:00Z';
-- Africa/Casablanca  row 249  intended 2026-11-29 12:00  currently shows 2026-11-29 11:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-29T12:00:00Z' WHERE "id" = 249 AND "starts_at" = '2026-11-29T11:00:00Z';
-- Africa/Casablanca  row 251  intended 2027-01-27 16:15  currently shows 2027-01-27 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-27T16:15:00Z' WHERE "id" = 251 AND "starts_at" = '2027-01-27T15:15:00Z';
-- Africa/Casablanca  row 253  intended 2027-05-26 11:00  currently shows 2027-05-26 10:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-26T11:00:00Z' WHERE "id" = 253 AND "starts_at" = '2027-05-26T10:00:00Z';
-- Africa/Casablanca  row 255  intended 2026-12-18 11:45  currently shows 2026-12-18 10:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-18T11:45:00Z' WHERE "id" = 255 AND "starts_at" = '2026-12-18T10:45:00Z';
-- Africa/Casablanca  row 256  intended 2027-12-19 10:45  currently shows 2027-12-19 09:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-19T10:45:00Z' WHERE "id" = 256 AND "starts_at" = '2027-12-19T09:45:00Z';
-- Africa/Casablanca  row 260  intended 2026-11-23 15:00  currently shows 2026-11-23 14:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-23T15:00:00Z' WHERE "id" = 260 AND "starts_at" = '2026-11-23T14:00:00Z';
-- Africa/Casablanca  row 266  intended 2026-10-30 10:00  currently shows 2026-10-30 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-30T10:00:00Z' WHERE "id" = 266 AND "starts_at" = '2026-10-30T09:00:00Z';
-- Africa/Casablanca  row 267  intended 2027-06-16 11:45  currently shows 2027-06-16 10:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-16T11:45:00Z' WHERE "id" = 267 AND "starts_at" = '2027-06-16T10:45:00Z';
-- Africa/Casablanca  row 268  intended 2027-05-30 15:45  currently shows 2027-05-30 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-30T15:45:00Z' WHERE "id" = 268 AND "starts_at" = '2027-05-30T14:45:00Z';
-- Africa/Casablanca  row 270  intended 2027-06-13 10:45  currently shows 2027-06-13 09:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-13T10:45:00Z' WHERE "id" = 270 AND "starts_at" = '2027-06-13T09:45:00Z';
-- Africa/Casablanca  row 274  intended 2026-12-26 17:00  currently shows 2026-12-26 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-26T17:00:00Z' WHERE "id" = 274 AND "starts_at" = '2026-12-26T16:00:00Z';
-- Africa/Casablanca  row 276  intended 2027-10-13 08:30  currently shows 2027-10-13 07:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-13T08:30:00Z' WHERE "id" = 276 AND "starts_at" = '2027-10-13T07:30:00Z';
-- Africa/Casablanca  row 278  intended 2027-01-05 17:00  currently shows 2027-01-05 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-05T17:00:00Z' WHERE "id" = 278 AND "starts_at" = '2027-01-05T16:00:00Z';
-- Africa/Casablanca  row 281  intended 2027-03-26 15:30  currently shows 2027-03-26 14:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-26T15:30:00Z' WHERE "id" = 281 AND "starts_at" = '2027-03-26T14:30:00Z';
-- Africa/Casablanca  row 283  intended 2027-10-19 14:15  currently shows 2027-10-19 13:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-19T14:15:00Z' WHERE "id" = 283 AND "starts_at" = '2027-10-19T13:15:00Z';
-- Africa/Casablanca  row 286  intended 2027-11-06 08:45  currently shows 2027-11-06 07:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-06T08:45:00Z' WHERE "id" = 286 AND "starts_at" = '2027-11-06T07:45:00Z';
-- Africa/Casablanca  row 288  intended 2026-11-02 08:30  currently shows 2026-11-02 07:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-02T08:30:00Z' WHERE "id" = 288 AND "starts_at" = '2026-11-02T07:30:00Z';
-- Africa/Casablanca  row 290  intended 2027-01-26 11:30  currently shows 2027-01-26 10:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-26T11:30:00Z' WHERE "id" = 290 AND "starts_at" = '2027-01-26T10:30:00Z';
-- Africa/Casablanca  row 297  intended 2027-10-30 17:00  currently shows 2027-10-30 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-30T17:00:00Z' WHERE "id" = 297 AND "starts_at" = '2027-10-30T16:00:00Z';
-- Africa/Casablanca  row 301  intended 2026-10-31 15:15  currently shows 2026-10-31 14:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-31T15:15:00Z' WHERE "id" = 301 AND "starts_at" = '2026-10-31T14:15:00Z';
-- Africa/Casablanca  row 303  intended 2027-11-23 15:00  currently shows 2027-11-23 14:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-23T15:00:00Z' WHERE "id" = 303 AND "starts_at" = '2027-11-23T14:00:00Z';
-- Africa/Casablanca  row 308  intended 2027-12-13 10:45  currently shows 2027-12-13 09:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-13T10:45:00Z' WHERE "id" = 308 AND "starts_at" = '2027-12-13T09:45:00Z';
-- Africa/Casablanca  row 314  intended 2027-08-17 12:30  currently shows 2027-08-17 11:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-17T12:30:00Z' WHERE "id" = 314 AND "starts_at" = '2027-08-17T11:30:00Z';
-- Africa/Casablanca  row 322  intended 2026-12-15 10:00  currently shows 2026-12-15 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-15T10:00:00Z' WHERE "id" = 322 AND "starts_at" = '2026-12-15T09:00:00Z';
-- Africa/Casablanca  row 324  intended 2027-11-10 12:45  currently shows 2027-11-10 11:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-10T12:45:00Z' WHERE "id" = 324 AND "starts_at" = '2027-11-10T11:45:00Z';
-- Africa/Casablanca  row 327  intended 2027-05-19 16:30  currently shows 2027-05-19 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-19T16:30:00Z' WHERE "id" = 327 AND "starts_at" = '2027-05-19T15:30:00Z';
-- Africa/Casablanca  row 329  intended 2027-03-19 17:00  currently shows 2027-03-19 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-19T17:00:00Z' WHERE "id" = 329 AND "starts_at" = '2027-03-19T16:00:00Z';
-- Africa/Casablanca  row 332  intended 2027-12-08 11:15  currently shows 2027-12-08 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-08T11:15:00Z' WHERE "id" = 332 AND "starts_at" = '2027-12-08T10:15:00Z';
-- Africa/Casablanca  row 339  intended 2027-11-28 09:30  currently shows 2027-11-28 08:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-28T09:30:00Z' WHERE "id" = 339 AND "starts_at" = '2027-11-28T08:30:00Z';
-- Africa/Casablanca  row 341  intended 2027-10-30 14:00  currently shows 2027-10-30 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-30T14:00:00Z' WHERE "id" = 341 AND "starts_at" = '2027-10-30T13:00:00Z';
-- Africa/Casablanca  row 342  intended 2027-05-07 08:15  currently shows 2027-05-07 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-07T08:15:00Z' WHERE "id" = 342 AND "starts_at" = '2027-05-07T07:15:00Z';
-- Africa/Casablanca  row 343  intended 2026-10-21 12:15  currently shows 2026-10-21 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-21T12:15:00Z' WHERE "id" = 343 AND "starts_at" = '2026-10-21T11:15:00Z';
-- Africa/Casablanca  row 347  intended 2027-06-28 14:00  currently shows 2027-06-28 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-28T14:00:00Z' WHERE "id" = 347 AND "starts_at" = '2027-06-28T13:00:00Z';
-- Africa/Casablanca  row 351  intended 2027-09-21 12:00  currently shows 2027-09-21 11:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-21T12:00:00Z' WHERE "id" = 351 AND "starts_at" = '2027-09-21T11:00:00Z';
-- Africa/Casablanca  row 353  intended 2027-12-03 10:00  currently shows 2027-12-03 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-03T10:00:00Z' WHERE "id" = 353 AND "starts_at" = '2027-12-03T09:00:00Z';
-- Africa/Casablanca  row 357  intended 2026-12-04 15:30  currently shows 2026-12-04 14:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-04T15:30:00Z' WHERE "id" = 357 AND "starts_at" = '2026-12-04T14:30:00Z';
-- Africa/Casablanca  row 364  intended 2026-11-08 16:15  currently shows 2026-11-08 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-08T16:15:00Z' WHERE "id" = 364 AND "starts_at" = '2026-11-08T15:15:00Z';
-- Africa/Casablanca  row 370  intended 2026-11-15 12:15  currently shows 2026-11-15 11:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-15T12:15:00Z' WHERE "id" = 370 AND "starts_at" = '2026-11-15T11:15:00Z';
-- Africa/Casablanca  row 371  intended 2026-12-03 10:30  currently shows 2026-12-03 09:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-03T10:30:00Z' WHERE "id" = 371 AND "starts_at" = '2026-12-03T09:30:00Z';
-- Africa/Casablanca  row 372  intended 2027-04-19 10:15  currently shows 2027-04-19 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-04-19T10:15:00Z' WHERE "id" = 372 AND "starts_at" = '2027-04-19T09:15:00Z';
-- Africa/Casablanca  row 373  intended 2026-12-19 15:45  currently shows 2026-12-19 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-19T15:45:00Z' WHERE "id" = 373 AND "starts_at" = '2026-12-19T14:45:00Z';
-- Africa/Casablanca  row 375  intended 2027-09-16 16:30  currently shows 2027-09-16 15:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-16T16:30:00Z' WHERE "id" = 375 AND "starts_at" = '2027-09-16T15:30:00Z';
-- Africa/Casablanca  row 377  intended 2027-12-08 12:30  currently shows 2027-12-08 11:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-08T12:30:00Z' WHERE "id" = 377 AND "starts_at" = '2027-12-08T11:30:00Z';
-- Africa/Casablanca  row 378  intended 2027-07-28 10:15  currently shows 2027-07-28 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-07-28T10:15:00Z' WHERE "id" = 378 AND "starts_at" = '2027-07-28T09:15:00Z';
-- Africa/Casablanca  row 379  intended 2027-05-07 09:45  currently shows 2027-05-07 08:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-07T09:45:00Z' WHERE "id" = 379 AND "starts_at" = '2027-05-07T08:45:00Z';
-- Africa/Casablanca  row 380  intended 2026-12-27 11:15  currently shows 2026-12-27 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-27T11:15:00Z' WHERE "id" = 380 AND "starts_at" = '2026-12-27T10:15:00Z';
-- Africa/Casablanca  row 385  intended 2027-12-19 15:15  currently shows 2027-12-19 14:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-19T15:15:00Z' WHERE "id" = 385 AND "starts_at" = '2027-12-19T14:15:00Z';
-- Africa/Casablanca  row 393  intended 2027-12-24 10:00  currently shows 2027-12-24 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-12-24T10:00:00Z' WHERE "id" = 393 AND "starts_at" = '2027-12-24T09:00:00Z';
-- Africa/Casablanca  row 396  intended 2026-11-05 10:30  currently shows 2026-11-05 09:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-05T10:30:00Z' WHERE "id" = 396 AND "starts_at" = '2026-11-05T09:30:00Z';
-- Africa/Casablanca  row 400  intended 2027-06-10 08:15  currently shows 2027-06-10 07:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-06-10T08:15:00Z' WHERE "id" = 400 AND "starts_at" = '2027-06-10T07:15:00Z';
-- Africa/El_Aaiun  row 4  intended 2026-12-04 15:45  currently shows 2026-12-04 14:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-04T15:45:00Z' WHERE "id" = 4 AND "starts_at" = '2026-12-04T14:45:00Z';
-- Africa/El_Aaiun  row 10  intended 2027-08-11 09:45  currently shows 2027-08-11 08:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-11T09:45:00Z' WHERE "id" = 10 AND "starts_at" = '2027-08-11T08:45:00Z';
-- Africa/El_Aaiun  row 37  intended 2027-08-10 09:00  currently shows 2027-08-10 08:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-08-10T09:00:00Z' WHERE "id" = 37 AND "starts_at" = '2027-08-10T08:00:00Z';
-- Africa/El_Aaiun  row 75  intended 2026-12-28 17:30  currently shows 2026-12-28 16:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-28T17:30:00Z' WHERE "id" = 75 AND "starts_at" = '2026-12-28T16:30:00Z';
-- Africa/El_Aaiun  row 77  intended 2026-10-05 14:45  currently shows 2026-10-05 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-05T14:45:00Z' WHERE "id" = 77 AND "starts_at" = '2026-10-05T13:45:00Z';
-- Africa/El_Aaiun  row 96  intended 2026-12-03 11:15  currently shows 2026-12-03 10:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-03T11:15:00Z' WHERE "id" = 96 AND "starts_at" = '2026-12-03T10:15:00Z';
-- Africa/El_Aaiun  row 106  intended 2027-05-04 14:45  currently shows 2027-05-04 13:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-04T14:45:00Z' WHERE "id" = 106 AND "starts_at" = '2027-05-04T13:45:00Z';
-- Africa/El_Aaiun  row 110  intended 2027-04-14 14:00  currently shows 2027-04-14 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-04-14T14:00:00Z' WHERE "id" = 110 AND "starts_at" = '2027-04-14T13:00:00Z';
-- Africa/El_Aaiun  row 116  intended 2026-12-10 09:15  currently shows 2026-12-10 08:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-10T09:15:00Z' WHERE "id" = 116 AND "starts_at" = '2026-12-10T08:15:00Z';
-- Africa/El_Aaiun  row 164  intended 2027-09-01 16:45  currently shows 2027-09-01 15:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-09-01T16:45:00Z' WHERE "id" = 164 AND "starts_at" = '2027-09-01T15:45:00Z';
-- Africa/El_Aaiun  row 179  intended 2027-05-17 08:00  currently shows 2027-05-17 07:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-17T08:00:00Z' WHERE "id" = 179 AND "starts_at" = '2027-05-17T07:00:00Z';
-- Africa/El_Aaiun  row 181  intended 2026-10-30 10:30  currently shows 2026-10-30 09:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-30T10:30:00Z' WHERE "id" = 181 AND "starts_at" = '2026-10-30T09:30:00Z';
-- Africa/El_Aaiun  row 217  intended 2026-11-30 12:30  currently shows 2026-11-30 11:30  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-30T12:30:00Z' WHERE "id" = 217 AND "starts_at" = '2026-11-30T11:30:00Z';
-- Africa/El_Aaiun  row 221  intended 2026-11-03 16:00  currently shows 2026-11-03 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-11-03T16:00:00Z' WHERE "id" = 221 AND "starts_at" = '2026-11-03T15:00:00Z';
-- Africa/El_Aaiun  row 296  intended 2027-10-13 16:00  currently shows 2027-10-13 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-10-13T16:00:00Z' WHERE "id" = 296 AND "starts_at" = '2027-10-13T15:00:00Z';
-- Africa/El_Aaiun  row 316  intended 2027-01-15 10:00  currently shows 2027-01-15 09:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-01-15T10:00:00Z' WHERE "id" = 316 AND "starts_at" = '2027-01-15T09:00:00Z';
-- Africa/El_Aaiun  row 323  intended 2026-12-11 09:45  currently shows 2026-12-11 08:45  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-12-11T09:45:00Z' WHERE "id" = 323 AND "starts_at" = '2026-12-11T08:45:00Z';
-- Africa/El_Aaiun  row 333  intended 2027-05-08 16:15  currently shows 2027-05-08 15:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-08T16:15:00Z' WHERE "id" = 333 AND "starts_at" = '2027-05-08T15:15:00Z';
-- Africa/El_Aaiun  row 345  intended 2027-05-10 14:00  currently shows 2027-05-10 13:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-05-10T14:00:00Z' WHERE "id" = 345 AND "starts_at" = '2027-05-10T13:00:00Z';
-- Africa/El_Aaiun  row 356  intended 2026-10-28 17:00  currently shows 2026-10-28 16:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2026-10-28T17:00:00Z' WHERE "id" = 356 AND "starts_at" = '2026-10-28T16:00:00Z';
-- Africa/El_Aaiun  row 360  intended 2027-03-31 16:00  currently shows 2027-03-31 15:00  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-03-31T16:00:00Z' WHERE "id" = 360 AND "starts_at" = '2027-03-31T15:00:00Z';
-- Africa/El_Aaiun  row 369  intended 2027-11-02 10:15  currently shows 2027-11-02 09:15  shift -1h
UPDATE "appointments" SET "starts_at" = '2027-11-02T10:15:00Z' WHERE "id" = 369 AND "starts_at" = '2027-11-02T09:15:00Z';
-- America/Edmonton  row 43  intended 2027-11-12 16:30  currently shows 2027-11-12 17:30  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-11-12T22:30:00Z' WHERE "id" = 43 AND "starts_at" = '2027-11-12T23:30:00Z';
-- America/Edmonton  row 50  intended 2027-11-27 16:30  currently shows 2027-11-27 17:30  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-11-27T22:30:00Z' WHERE "id" = 50 AND "starts_at" = '2027-11-27T23:30:00Z';
-- America/Edmonton  row 58  intended 2026-11-17 17:00  currently shows 2026-11-17 18:00  shift +1h
UPDATE "appointments" SET "starts_at" = '2026-11-17T23:00:00Z' WHERE "id" = 58 AND "starts_at" = '2026-11-18T00:00:00Z';
-- America/Edmonton  row 76  intended 2027-11-11 09:30  currently shows 2027-11-11 10:30  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-11-11T15:30:00Z' WHERE "id" = 76 AND "starts_at" = '2027-11-11T16:30:00Z';
-- America/Edmonton  row 132  intended 2027-03-12 12:15  currently shows 2027-03-12 13:15  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-03-12T18:15:00Z' WHERE "id" = 132 AND "starts_at" = '2027-03-12T19:15:00Z';
-- America/Edmonton  row 188  intended 2027-01-11 17:30  currently shows 2027-01-11 18:30  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-01-11T23:30:00Z' WHERE "id" = 188 AND "starts_at" = '2027-01-12T00:30:00Z';
-- America/Edmonton  row 269  intended 2027-01-16 15:15  currently shows 2027-01-16 16:15  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-01-16T21:15:00Z' WHERE "id" = 269 AND "starts_at" = '2027-01-16T22:15:00Z';
-- America/Edmonton  row 381  intended 2027-12-14 12:00  currently shows 2027-12-14 13:00  shift +1h
UPDATE "appointments" SET "starts_at" = '2027-12-14T18:00:00Z' WHERE "id" = 381 AND "starts_at" = '2027-12-14T19:00:00Z';
COMMIT;
