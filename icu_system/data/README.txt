This archive contains reconstructed DDL for all 31 eICU-CRD tables listed on the MIT-LCP SchemaSpy site.

Files
- schema_postgresql_31_tables.sql
- schema_sqlite_31_tables.sql

Coverage
- 31 CREATE TABLE statements
- hospital + patient first, then remaining 29 patient-linked tables
- 29 foreign keys from *.patientunitstayid -> patient.patientunitstayid, as shown on the SchemaSpy patient page
- a practical FK from patient.hospitalid -> hospital.hospitalid
- patient.patientunitstayid set as PRIMARY KEY because the patient page explicitly shows it
- hospital.hospitalid set as PRIMARY KEY for practical initialization

Important note
SchemaSpy clearly exposes the column layouts and patientunitstayid relationships. It does not clearly expose a primary key for every table in the text rendering available here, so this DDL is intentionally conservative rather than inventing undocumented PK constraints across all tables.
