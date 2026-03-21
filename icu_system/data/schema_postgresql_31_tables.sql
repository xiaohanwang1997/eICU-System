-- eICU-CRD Schema DDL reconstructed from MIT-LCP SchemaSpy table pages
-- Source: https://lcp.mit.edu/eicu-schema-spy/ (generated Aug 8, 2019)
-- Tables included: 31
-- Note: patient.patientunitstayid is the only primary key explicitly shown on the patient page;
-- this script adds the 29 patientunitstayid foreign keys shown in SchemaSpy and a practical PK on hospitalid for usability.

DROP TABLE IF EXISTS hospital CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS admissiondrug CASCADE;
DROP TABLE IF EXISTS admissiondx CASCADE;
DROP TABLE IF EXISTS allergy CASCADE;
DROP TABLE IF EXISTS apacheapsvar CASCADE;
DROP TABLE IF EXISTS apachepatientresult CASCADE;
DROP TABLE IF EXISTS apachepredvar CASCADE;
DROP TABLE IF EXISTS careplancareprovider CASCADE;
DROP TABLE IF EXISTS careplaneol CASCADE;
DROP TABLE IF EXISTS careplangeneral CASCADE;
DROP TABLE IF EXISTS careplangoal CASCADE;
DROP TABLE IF EXISTS careplaninfectiousdisease CASCADE;
DROP TABLE IF EXISTS customlab CASCADE;
DROP TABLE IF EXISTS diagnosis CASCADE;
DROP TABLE IF EXISTS infusiondrug CASCADE;
DROP TABLE IF EXISTS intakeoutput CASCADE;
DROP TABLE IF EXISTS lab CASCADE;
DROP TABLE IF EXISTS medication CASCADE;
DROP TABLE IF EXISTS microlab CASCADE;
DROP TABLE IF EXISTS note CASCADE;
DROP TABLE IF EXISTS nurseassessment CASCADE;
DROP TABLE IF EXISTS nursecare CASCADE;
DROP TABLE IF EXISTS nursecharting CASCADE;
DROP TABLE IF EXISTS pasthistory CASCADE;
DROP TABLE IF EXISTS physicalexam CASCADE;
DROP TABLE IF EXISTS respiratorycare CASCADE;
DROP TABLE IF EXISTS respiratorycharting CASCADE;
DROP TABLE IF EXISTS treatment CASCADE;
DROP TABLE IF EXISTS vitalaperiodic CASCADE;
DROP TABLE IF EXISTS vitalperiodic CASCADE;

CREATE TABLE hospital (
    hospitalid INTEGER PRIMARY KEY,
    numbedscategory VARCHAR(32),
    teachingstatus BOOLEAN,
    region VARCHAR(64)
);

CREATE TABLE patient (
    patientunitstayid INTEGER PRIMARY KEY,
    patienthealthsystemstayid INTEGER,
    gender VARCHAR(25),
    age VARCHAR(10),
    ethnicity VARCHAR(50),
    hospitalid INTEGER,
    wardid INTEGER,
    apacheadmissiondx VARCHAR(1000),
    admissionheight NUMERIC(10,2),
    hospitaladmittime24 VARCHAR(8),
    hospitaladmitoffset INTEGER,
    hospitaladmitsource VARCHAR(30),
    hospitaldischargeyear SMALLINT,
    hospitaldischargetime24 VARCHAR(8),
    hospitaldischargeoffset INTEGER,
    hospitaldischargelocation VARCHAR(100),
    hospitaldischargestatus VARCHAR(10),
    unittype VARCHAR(50),
    unitadmittime24 VARCHAR(8),
    unitadmitsource VARCHAR(100),
    unitvisitnumber INTEGER,
    unitstaytype VARCHAR(15),
    admissionweight NUMERIC(10,2),
    dischargeweight NUMERIC(10,2),
    unitdischargetime24 VARCHAR(8),
    unitdischargeoffset INTEGER,
    unitdischargelocation VARCHAR(100),
    unitdischargestatus VARCHAR(10),
    uniquepid VARCHAR(10),
    FOREIGN KEY (hospitalid) REFERENCES hospital(hospitalid)
);

CREATE TABLE admissiondrug (
    admissiondrugid INTEGER,
    patientunitstayid INTEGER,
    drugoffset INTEGER,
    drugenteredoffset INTEGER,
    drugnotetype VARCHAR(255),
    specialtytype VARCHAR(255),
    usertype VARCHAR(255),
    rxincluded VARCHAR(5),
    writtenineicu VARCHAR(5),
    drugname VARCHAR(255),
    drugdosage NUMERIC(11,4),
    drugunit VARCHAR(1000),
    drugadmitfrequency VARCHAR(1000),
    drughiclseqno INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE admissiondx (
    admissiondxid INTEGER,
    patientunitstayid INTEGER,
    admitdxenteredoffset INTEGER,
    admitdxpath VARCHAR(500),
    admitdxname VARCHAR(255),
    admitdxtext VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE allergy (
    allergyid INTEGER,
    patientunitstayid INTEGER,
    allergyoffset INTEGER,
    allergyenteredoffset INTEGER,
    allergynotetype VARCHAR(255),
    specialtytype VARCHAR(255),
    usertype VARCHAR(255),
    rxincluded VARCHAR(5),
    writtenineicu VARCHAR(5),
    drugname VARCHAR(255),
    allergytype VARCHAR(255),
    allergyname VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apacheapsvar (
    apacheapsvarid INTEGER,
    patientunitstayid INTEGER,
    intubated SMALLINT,
    vent SMALLINT,
    dialysis SMALLINT,
    eyes SMALLINT,
    motor SMALLINT,
    verbal SMALLINT,
    meds SMALLINT,
    urine DOUBLE PRECISION,
    wbc DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    respiratoryrate DOUBLE PRECISION,
    sodium DOUBLE PRECISION,
    heartrate DOUBLE PRECISION,
    meanbp DOUBLE PRECISION,
    ph DOUBLE PRECISION,
    hematocrit DOUBLE PRECISION,
    creatinine DOUBLE PRECISION,
    albumin DOUBLE PRECISION,
    pao2 DOUBLE PRECISION,
    pco2 DOUBLE PRECISION,
    bun DOUBLE PRECISION,
    glucose DOUBLE PRECISION,
    bilirubin DOUBLE PRECISION,
    fio2 DOUBLE PRECISION,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apachepatientresult (
    apachepatientresultsid INTEGER,
    patientunitstayid INTEGER,
    physicianspeciality VARCHAR(50),
    physicianinterventioncategory VARCHAR(50),
    acutephysiologyscore INTEGER,
    apachescore INTEGER,
    apacheversion VARCHAR(5),
    predictedicumortality VARCHAR(50),
    actualicumortality VARCHAR(50),
    predictediculos DOUBLE PRECISION,
    actualiculos DOUBLE PRECISION,
    predictedhospitalmortality VARCHAR(50),
    actualhospitalmortality VARCHAR(50),
    predictedhospitallos DOUBLE PRECISION,
    actualhospitallos DOUBLE PRECISION,
    preopmi INTEGER,
    preopcardiaccath INTEGER,
    ptcawithin24h INTEGER,
    unabridgedunitlos DOUBLE PRECISION,
    unabridgedhosplos DOUBLE PRECISION,
    actualventdays DOUBLE PRECISION,
    predventdays DOUBLE PRECISION,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apachepredvar (
    apachepredvarid INTEGER,
    patientunitstayid INTEGER,
    sicuday SMALLINT,
    saps3day1 SMALLINT,
    saps3today SMALLINT,
    saps3yesterday SMALLINT,
    gender SMALLINT,
    teachtype SMALLINT,
    region SMALLINT,
    bedcount SMALLINT,
    admitsource SMALLINT,
    graftcount SMALLINT,
    meds SMALLINT,
    verbal SMALLINT,
    motor SMALLINT,
    eyes SMALLINT,
    age SMALLINT,
    admitdiagnosis VARCHAR(11),
    thrombolytics SMALLINT,
    diedinhospital SMALLINT,
    aids SMALLINT,
    hepaticfailure SMALLINT,
    lymphoma SMALLINT,
    metastaticcancer SMALLINT,
    leukemia SMALLINT,
    immunosuppression SMALLINT,
    cirrhosis SMALLINT,
    electivesurgery SMALLINT,
    activetx SMALLINT,
    readmit SMALLINT,
    ima SMALLINT,
    midur SMALLINT,
    ventday1 SMALLINT,
    oobventday1 SMALLINT,
    oobintubday1 SMALLINT,
    diabetes SMALLINT,
    managementsystem SMALLINT,
    var03hspxlos DOUBLE PRECISION,
    pao2 DOUBLE PRECISION,
    fio2 DOUBLE PRECISION,
    ejectfx DOUBLE PRECISION,
    creatinine DOUBLE PRECISION,
    dischargelocation SMALLINT,
    visitnumber SMALLINT,
    amilocation SMALLINT,
    day1meds SMALLINT,
    day1verbal SMALLINT,
    day1motor SMALLINT,
    day1eyes SMALLINT,
    day1pao2 DOUBLE PRECISION,
    day1fio2 DOUBLE PRECISION,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplancareprovider (
    cplcareprovderid INTEGER,
    patientunitstayid INTEGER,
    careprovidersaveoffset INTEGER,
    providertype VARCHAR(255),
    specialty VARCHAR(255),
    interventioncategory VARCHAR(255),
    managingphysician VARCHAR(50),
    activeupondischarge VARCHAR(10),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplaneol (
    cpleolid INTEGER,
    patientunitstayid INTEGER,
    cpleolsaveoffset INTEGER,
    cpleoldiscussionoffset INTEGER,
    activeupondischarge VARCHAR(10),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplangeneral (
    cplgeneralid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge VARCHAR(10),
    cplitemoffset INTEGER,
    cplgroup VARCHAR(255),
    cplitemvalue VARCHAR(1024),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplangoal (
    cplgoalid INTEGER,
    patientunitstayid INTEGER,
    cplgoaloffset INTEGER,
    cplgoalcategory VARCHAR(255),
    cplgoalvalue VARCHAR(1000),
    cplgoalstatus VARCHAR(255),
    activeupondischarge VARCHAR(10),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplaninfectiousdisease (
    cplinfectid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge VARCHAR(10),
    cplinfectdiseaseoffset INTEGER,
    infectdiseasesite VARCHAR(64),
    infectdiseaseassessment VARCHAR(64),
    responsetotherapy VARCHAR(32),
    treatment VARCHAR(32),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE customlab (
    customlabid INTEGER,
    patientunitstayid INTEGER,
    labotheroffset INTEGER,
    labothertypeid INTEGER,
    labothername VARCHAR(64),
    labotherresult VARCHAR(64),
    labothervaluetext VARCHAR(128),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE diagnosis (
    diagnosisid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge VARCHAR(64),
    diagnosisoffset INTEGER,
    diagnosisstring VARCHAR(200),
    icd9code VARCHAR(100),
    diagnosispriority VARCHAR(10),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE infusiondrug (
    infusiondrugid INTEGER,
    patientunitstayid INTEGER,
    infusionoffset INTEGER,
    drugname VARCHAR(255),
    drugrate VARCHAR(255),
    infusionrate VARCHAR(255),
    drugamount VARCHAR(255),
    volumeoffluid VARCHAR(255),
    patientweight VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE intakeoutput (
    intakeoutputid INTEGER,
    patientunitstayid INTEGER,
    intakeoutputoffset INTEGER,
    intaketotal NUMERIC(12,4),
    outputtotal NUMERIC(12,4),
    dialysistotal NUMERIC(12,4),
    nettotal NUMERIC(12,4),
    intakeoutputentryoffset INTEGER,
    cellpath VARCHAR(500),
    celllabel VARCHAR(255),
    cellvaluenumeric NUMERIC(12,4),
    cellvaluetext VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE lab (
    labid INTEGER,
    patientunitstayid INTEGER,
    labresultoffset INTEGER,
    labtypeid NUMERIC(3),
    labname VARCHAR(256),
    labresult NUMERIC(11,4),
    labresulttext VARCHAR(255),
    labmeasurenamesystem VARCHAR(255),
    labmeasurenameinterface VARCHAR(255),
    labresultrevisedoffset INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE medication (
    medicationid INTEGER,
    patientunitstayid INTEGER,
    drugorderoffset INTEGER,
    drugstartoffset INTEGER,
    drugivadmixture VARCHAR(6),
    drugordercancelled VARCHAR(6),
    drugname VARCHAR(220),
    drughiclseqno INTEGER,
    dosage VARCHAR(60),
    routeadmin VARCHAR(120),
    frequency VARCHAR(255),
    loadingdose VARCHAR(120),
    prn VARCHAR(6),
    drugstopoffset INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE microlab (
    microlabid INTEGER,
    patientunitstayid INTEGER,
    culturetakenoffset INTEGER,
    culturesite VARCHAR(255),
    organism VARCHAR(255),
    antibiotic VARCHAR(255),
    sensitivitylevel VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE note (
    noteid INTEGER,
    patientunitstayid INTEGER,
    noteoffset INTEGER,
    noteenteredoffset INTEGER,
    notetype VARCHAR(50),
    notepath VARCHAR(255),
    notevalue VARCHAR(150),
    notetext VARCHAR(500),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nurseassessment (
    nurseassessid INTEGER,
    patientunitstayid INTEGER,
    nurseassessoffset INTEGER,
    nurseassessentryoffset INTEGER,
    cellattributepath VARCHAR(255),
    celllabel VARCHAR(255),
    cellattribute VARCHAR(255),
    cellattributevalue VARCHAR(4000),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nursecare (
    nursecareid INTEGER,
    patientunitstayid INTEGER,
    celllabel VARCHAR(255),
    nursecareoffset INTEGER,
    nursecareentryoffset INTEGER,
    cellattributepath VARCHAR(255),
    cellattribute VARCHAR(255),
    cellattributevalue VARCHAR(4000),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nursecharting (
    nursingchartid BIGINT,
    patientunitstayid INTEGER,
    nursingchartoffset INTEGER,
    nursingchartentryoffset INTEGER,
    nursingchartcelltypecat VARCHAR(255),
    nursingchartcelltypevallabel VARCHAR(255),
    nursingchartcelltypevalname VARCHAR(255),
    nursingchartvalue VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE pasthistory (
    pasthistoryid INTEGER,
    patientunitstayid INTEGER,
    pasthistoryoffset INTEGER,
    pasthistoryenteredoffset INTEGER,
    pasthistorynotetype VARCHAR(40),
    pasthistorypath VARCHAR(255),
    pasthistoryvalue VARCHAR(100),
    pasthistoryvaluetext VARCHAR(255),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE physicalexam (
    physicalexamid INTEGER,
    patientunitstayid INTEGER,
    physicalexamoffset INTEGER,
    physicalexampath VARCHAR(255),
    physicalexamvalue VARCHAR(100),
    physicalexamtext VARCHAR(500),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE respiratorycare (
    respcareid INTEGER,
    patientunitstayid INTEGER,
    respcarestatusoffset INTEGER,
    currenthistoryseqnum INTEGER,
    airwaytype VARCHAR(30),
    airwaysize VARCHAR(10),
    airwayposition VARCHAR(32),
    cuffpressure NUMERIC(5,1),
    ventstartoffset INTEGER,
    ventendoffset INTEGER,
    priorventstartoffset INTEGER,
    priorventendoffset INTEGER,
    apneaparams VARCHAR(80),
    lowexhmvlimit NUMERIC(11,4),
    hiexhmvlimit NUMERIC(11,4),
    lowexhtvlimit NUMERIC(11,4),
    hipeakpreslimit NUMERIC(11,4),
    lowpeakpreslimit NUMERIC(11,4),
    hirespratelimit NUMERIC(11,4),
    lowrespratelimit NUMERIC(11,4),
    sighpreslimit NUMERIC(11,4),
    lowironoxlimit NUMERIC(11,4),
    highironoxlimit NUMERIC(11,4),
    meanairwaypreslimit NUMERIC(11,4),
    peeplimit NUMERIC(11,4),
    cpaplimit NUMERIC(11,4),
    setapneainterval VARCHAR(80),
    setapneatv VARCHAR(80),
    setapneaippeephigh VARCHAR(80),
    setapnearr VARCHAR(80),
    setapneapeakflow VARCHAR(80),
    setapneainsptime VARCHAR(80),
    setapneaie VARCHAR(80),
    setapneafio2 VARCHAR(80),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE respiratorycharting (
    respchartid INTEGER,
    patientunitstayid INTEGER,
    respchartoffset INTEGER,
    respchartentryoffset INTEGER,
    respcharttypecat VARCHAR(255),
    respchartvaluelabel VARCHAR(255),
    respchartvalue VARCHAR(1000),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE treatment (
    treatmentid INTEGER,
    patientunitstayid INTEGER,
    treatmentoffset INTEGER,
    treatmentstring VARCHAR(200),
    activeupondischarge VARCHAR(10),
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE vitalaperiodic (
    vitalaperiodicid INTEGER,
    patientunitstayid INTEGER,
    observationoffset INTEGER,
    noninvasivesystolic DOUBLE PRECISION,
    noninvasivediastolic DOUBLE PRECISION,
    noninvasivemean DOUBLE PRECISION,
    paop DOUBLE PRECISION,
    cardiacoutput DOUBLE PRECISION,
    cardiacinput DOUBLE PRECISION,
    svr DOUBLE PRECISION,
    svri DOUBLE PRECISION,
    pvr DOUBLE PRECISION,
    pvri DOUBLE PRECISION,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE vitalperiodic (
    vitalperiodicid BIGINT,
    patientunitstayid INTEGER,
    observationoffset INTEGER,
    temperature NUMERIC(11,4),
    sao2 INTEGER,
    heartrate INTEGER,
    respiration INTEGER,
    cvp INTEGER,
    etco2 INTEGER,
    systemicsystolic INTEGER,
    systemicdiastolic INTEGER,
    systemicmean INTEGER,
    pasystolic INTEGER,
    padiastolic INTEGER,
    pamean INTEGER,
    st1 DOUBLE PRECISION,
    st2 DOUBLE PRECISION,
    st3 DOUBLE PRECISION,
    icp INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);
