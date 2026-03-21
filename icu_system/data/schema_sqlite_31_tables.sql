-- eICU-CRD Schema DDL reconstructed from MIT-LCP SchemaSpy table pages
-- Source: https://lcp.mit.edu/eicu-schema-spy/ (generated Aug 8, 2019)
-- Tables included: 31
-- Note: patient.patientunitstayid is the only primary key explicitly shown on the patient page;
-- this script adds the 29 patientunitstayid foreign keys shown in SchemaSpy and a practical PK on hospitalid for usability.

DROP TABLE IF EXISTS hospital;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS admissiondrug;
DROP TABLE IF EXISTS admissiondx;
DROP TABLE IF EXISTS allergy;
DROP TABLE IF EXISTS apacheapsvar;
DROP TABLE IF EXISTS apachepatientresult;
DROP TABLE IF EXISTS apachepredvar;
DROP TABLE IF EXISTS careplancareprovider;
DROP TABLE IF EXISTS careplaneol;
DROP TABLE IF EXISTS careplangeneral;
DROP TABLE IF EXISTS careplangoal;
DROP TABLE IF EXISTS careplaninfectiousdisease;
DROP TABLE IF EXISTS customlab;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS infusiondrug;
DROP TABLE IF EXISTS intakeoutput;
DROP TABLE IF EXISTS lab;
DROP TABLE IF EXISTS medication;
DROP TABLE IF EXISTS microlab;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS nurseassessment;
DROP TABLE IF EXISTS nursecare;
DROP TABLE IF EXISTS nursecharting;
DROP TABLE IF EXISTS pasthistory;
DROP TABLE IF EXISTS physicalexam;
DROP TABLE IF EXISTS respiratorycare;
DROP TABLE IF EXISTS respiratorycharting;
DROP TABLE IF EXISTS treatment;
DROP TABLE IF EXISTS vitalaperiodic;
DROP TABLE IF EXISTS vitalperiodic;

CREATE TABLE hospital (
    hospitalid INTEGER PRIMARY KEY,
    numbedscategory TEXT,
    teachingstatus INTEGER,
    region TEXT
);

CREATE TABLE patient (
    patientunitstayid INTEGER PRIMARY KEY,
    patienthealthsystemstayid INTEGER,
    gender TEXT,
    age TEXT,
    ethnicity TEXT,
    hospitalid INTEGER,
    wardid INTEGER,
    apacheadmissiondx TEXT,
    admissionheight NUMERIC,
    hospitaladmittime24 TEXT,
    hospitaladmitoffset INTEGER,
    hospitaladmitsource TEXT,
    hospitaldischargeyear INTEGER,
    hospitaldischargetime24 TEXT,
    hospitaldischargeoffset INTEGER,
    hospitaldischargelocation TEXT,
    hospitaldischargestatus TEXT,
    unittype TEXT,
    unitadmittime24 TEXT,
    unitadmitsource TEXT,
    unitvisitnumber INTEGER,
    unitstaytype TEXT,
    admissionweight NUMERIC,
    dischargeweight NUMERIC,
    unitdischargetime24 TEXT,
    unitdischargeoffset INTEGER,
    unitdischargelocation TEXT,
    unitdischargestatus TEXT,
    uniquepid TEXT,
    FOREIGN KEY (hospitalid) REFERENCES hospital(hospitalid)
);

CREATE TABLE admissiondrug (
    admissiondrugid INTEGER,
    patientunitstayid INTEGER,
    drugoffset INTEGER,
    drugenteredoffset INTEGER,
    drugnotetype TEXT,
    specialtytype TEXT,
    usertype TEXT,
    rxincluded TEXT,
    writtenineicu TEXT,
    drugname TEXT,
    drugdosage NUMERIC,
    drugunit TEXT,
    drugadmitfrequency TEXT,
    drughiclseqno INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE admissiondx (
    admissiondxid INTEGER,
    patientunitstayid INTEGER,
    admitdxenteredoffset INTEGER,
    admitdxpath TEXT,
    admitdxname TEXT,
    admitdxtext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE allergy (
    allergyid INTEGER,
    patientunitstayid INTEGER,
    allergyoffset INTEGER,
    allergyenteredoffset INTEGER,
    allergynotetype TEXT,
    specialtytype TEXT,
    usertype TEXT,
    rxincluded TEXT,
    writtenineicu TEXT,
    drugname TEXT,
    allergytype TEXT,
    allergyname TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apacheapsvar (
    apacheapsvarid INTEGER,
    patientunitstayid INTEGER,
    intubated INTEGER,
    vent INTEGER,
    dialysis INTEGER,
    eyes INTEGER,
    motor INTEGER,
    verbal INTEGER,
    meds INTEGER,
    urine REAL,
    wbc REAL,
    temperature REAL,
    respiratoryrate REAL,
    sodium REAL,
    heartrate REAL,
    meanbp REAL,
    ph REAL,
    hematocrit REAL,
    creatinine REAL,
    albumin REAL,
    pao2 REAL,
    pco2 REAL,
    bun REAL,
    glucose REAL,
    bilirubin REAL,
    fio2 REAL,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apachepatientresult (
    apachepatientresultsid INTEGER,
    patientunitstayid INTEGER,
    physicianspeciality TEXT,
    physicianinterventioncategory TEXT,
    acutephysiologyscore INTEGER,
    apachescore INTEGER,
    apacheversion TEXT,
    predictedicumortality TEXT,
    actualicumortality TEXT,
    predictediculos REAL,
    actualiculos REAL,
    predictedhospitalmortality TEXT,
    actualhospitalmortality TEXT,
    predictedhospitallos REAL,
    actualhospitallos REAL,
    preopmi INTEGER,
    preopcardiaccath INTEGER,
    ptcawithin24h INTEGER,
    unabridgedunitlos REAL,
    unabridgedhosplos REAL,
    actualventdays REAL,
    predventdays REAL,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE apachepredvar (
    apachepredvarid INTEGER,
    patientunitstayid INTEGER,
    sicuday INTEGER,
    saps3day1 INTEGER,
    saps3today INTEGER,
    saps3yesterday INTEGER,
    gender INTEGER,
    teachtype INTEGER,
    region INTEGER,
    bedcount INTEGER,
    admitsource INTEGER,
    graftcount INTEGER,
    meds INTEGER,
    verbal INTEGER,
    motor INTEGER,
    eyes INTEGER,
    age INTEGER,
    admitdiagnosis TEXT,
    thrombolytics INTEGER,
    diedinhospital INTEGER,
    aids INTEGER,
    hepaticfailure INTEGER,
    lymphoma INTEGER,
    metastaticcancer INTEGER,
    leukemia INTEGER,
    immunosuppression INTEGER,
    cirrhosis INTEGER,
    electivesurgery INTEGER,
    activetx INTEGER,
    readmit INTEGER,
    ima INTEGER,
    midur INTEGER,
    ventday1 INTEGER,
    oobventday1 INTEGER,
    oobintubday1 INTEGER,
    diabetes INTEGER,
    managementsystem INTEGER,
    var03hspxlos REAL,
    pao2 REAL,
    fio2 REAL,
    ejectfx REAL,
    creatinine REAL,
    dischargelocation INTEGER,
    visitnumber INTEGER,
    amilocation INTEGER,
    day1meds INTEGER,
    day1verbal INTEGER,
    day1motor INTEGER,
    day1eyes INTEGER,
    day1pao2 REAL,
    day1fio2 REAL,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplancareprovider (
    cplcareprovderid INTEGER,
    patientunitstayid INTEGER,
    careprovidersaveoffset INTEGER,
    providertype TEXT,
    specialty TEXT,
    interventioncategory TEXT,
    managingphysician TEXT,
    activeupondischarge TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplaneol (
    cpleolid INTEGER,
    patientunitstayid INTEGER,
    cpleolsaveoffset INTEGER,
    cpleoldiscussionoffset INTEGER,
    activeupondischarge TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplangeneral (
    cplgeneralid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge TEXT,
    cplitemoffset INTEGER,
    cplgroup TEXT,
    cplitemvalue TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplangoal (
    cplgoalid INTEGER,
    patientunitstayid INTEGER,
    cplgoaloffset INTEGER,
    cplgoalcategory TEXT,
    cplgoalvalue TEXT,
    cplgoalstatus TEXT,
    activeupondischarge TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE careplaninfectiousdisease (
    cplinfectid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge TEXT,
    cplinfectdiseaseoffset INTEGER,
    infectdiseasesite TEXT,
    infectdiseaseassessment TEXT,
    responsetotherapy TEXT,
    treatment TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE customlab (
    customlabid INTEGER,
    patientunitstayid INTEGER,
    labotheroffset INTEGER,
    labothertypeid INTEGER,
    labothername TEXT,
    labotherresult TEXT,
    labothervaluetext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE diagnosis (
    diagnosisid INTEGER,
    patientunitstayid INTEGER,
    activeupondischarge TEXT,
    diagnosisoffset INTEGER,
    diagnosisstring TEXT,
    icd9code TEXT,
    diagnosispriority TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE infusiondrug (
    infusiondrugid INTEGER,
    patientunitstayid INTEGER,
    infusionoffset INTEGER,
    drugname TEXT,
    drugrate TEXT,
    infusionrate TEXT,
    drugamount TEXT,
    volumeoffluid TEXT,
    patientweight TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE intakeoutput (
    intakeoutputid INTEGER,
    patientunitstayid INTEGER,
    intakeoutputoffset INTEGER,
    intaketotal NUMERIC,
    outputtotal NUMERIC,
    dialysistotal NUMERIC,
    nettotal NUMERIC,
    intakeoutputentryoffset INTEGER,
    cellpath TEXT,
    celllabel TEXT,
    cellvaluenumeric NUMERIC,
    cellvaluetext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE lab (
    labid INTEGER,
    patientunitstayid INTEGER,
    labresultoffset INTEGER,
    labtypeid NUMERIC,
    labname TEXT,
    labresult NUMERIC,
    labresulttext TEXT,
    labmeasurenamesystem TEXT,
    labmeasurenameinterface TEXT,
    labresultrevisedoffset INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE medication (
    medicationid INTEGER,
    patientunitstayid INTEGER,
    drugorderoffset INTEGER,
    drugstartoffset INTEGER,
    drugivadmixture TEXT,
    drugordercancelled TEXT,
    drugname TEXT,
    drughiclseqno INTEGER,
    dosage TEXT,
    routeadmin TEXT,
    frequency TEXT,
    loadingdose TEXT,
    prn TEXT,
    drugstopoffset INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE microlab (
    microlabid INTEGER,
    patientunitstayid INTEGER,
    culturetakenoffset INTEGER,
    culturesite TEXT,
    organism TEXT,
    antibiotic TEXT,
    sensitivitylevel TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE note (
    noteid INTEGER,
    patientunitstayid INTEGER,
    noteoffset INTEGER,
    noteenteredoffset INTEGER,
    notetype TEXT,
    notepath TEXT,
    notevalue TEXT,
    notetext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nurseassessment (
    nurseassessid INTEGER,
    patientunitstayid INTEGER,
    nurseassessoffset INTEGER,
    nurseassessentryoffset INTEGER,
    cellattributepath TEXT,
    celllabel TEXT,
    cellattribute TEXT,
    cellattributevalue TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nursecare (
    nursecareid INTEGER,
    patientunitstayid INTEGER,
    celllabel TEXT,
    nursecareoffset INTEGER,
    nursecareentryoffset INTEGER,
    cellattributepath TEXT,
    cellattribute TEXT,
    cellattributevalue TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE nursecharting (
    nursingchartid INTEGER,
    patientunitstayid INTEGER,
    nursingchartoffset INTEGER,
    nursingchartentryoffset INTEGER,
    nursingchartcelltypecat TEXT,
    nursingchartcelltypevallabel TEXT,
    nursingchartcelltypevalname TEXT,
    nursingchartvalue TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE pasthistory (
    pasthistoryid INTEGER,
    patientunitstayid INTEGER,
    pasthistoryoffset INTEGER,
    pasthistoryenteredoffset INTEGER,
    pasthistorynotetype TEXT,
    pasthistorypath TEXT,
    pasthistoryvalue TEXT,
    pasthistoryvaluetext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE physicalexam (
    physicalexamid INTEGER,
    patientunitstayid INTEGER,
    physicalexamoffset INTEGER,
    physicalexampath TEXT,
    physicalexamvalue TEXT,
    physicalexamtext TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE respiratorycare (
    respcareid INTEGER,
    patientunitstayid INTEGER,
    respcarestatusoffset INTEGER,
    currenthistoryseqnum INTEGER,
    airwaytype TEXT,
    airwaysize TEXT,
    airwayposition TEXT,
    cuffpressure NUMERIC,
    ventstartoffset INTEGER,
    ventendoffset INTEGER,
    priorventstartoffset INTEGER,
    priorventendoffset INTEGER,
    apneaparams TEXT,
    lowexhmvlimit NUMERIC,
    hiexhmvlimit NUMERIC,
    lowexhtvlimit NUMERIC,
    hipeakpreslimit NUMERIC,
    lowpeakpreslimit NUMERIC,
    hirespratelimit NUMERIC,
    lowrespratelimit NUMERIC,
    sighpreslimit NUMERIC,
    lowironoxlimit NUMERIC,
    highironoxlimit NUMERIC,
    meanairwaypreslimit NUMERIC,
    peeplimit NUMERIC,
    cpaplimit NUMERIC,
    setapneainterval TEXT,
    setapneatv TEXT,
    setapneaippeephigh TEXT,
    setapnearr TEXT,
    setapneapeakflow TEXT,
    setapneainsptime TEXT,
    setapneaie TEXT,
    setapneafio2 TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE respiratorycharting (
    respchartid INTEGER,
    patientunitstayid INTEGER,
    respchartoffset INTEGER,
    respchartentryoffset INTEGER,
    respcharttypecat TEXT,
    respchartvaluelabel TEXT,
    respchartvalue TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE treatment (
    treatmentid INTEGER,
    patientunitstayid INTEGER,
    treatmentoffset INTEGER,
    treatmentstring TEXT,
    activeupondischarge TEXT,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE vitalaperiodic (
    vitalaperiodicid INTEGER,
    patientunitstayid INTEGER,
    observationoffset INTEGER,
    noninvasivesystolic REAL,
    noninvasivediastolic REAL,
    noninvasivemean REAL,
    paop REAL,
    cardiacoutput REAL,
    cardiacinput REAL,
    svr REAL,
    svri REAL,
    pvr REAL,
    pvri REAL,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);

CREATE TABLE vitalperiodic (
    vitalperiodicid INTEGER,
    patientunitstayid INTEGER,
    observationoffset INTEGER,
    temperature NUMERIC,
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
    st1 REAL,
    st2 REAL,
    st3 REAL,
    icp INTEGER,
    FOREIGN KEY (patientunitstayid) REFERENCES patient(patientunitstayid)
);
