# MTP_CloudComputingLabs
This repo wil be used to maintain all the works related to CS797 MTP on Cloud Computing labs

```mermaid
graph TD
  A[Start] --> B[Read /home/labDirectory/data.json\n& secret-key.pem & ans.json]
  B --> C{public-ip present?}
  C -- No --> F1[Record SSH Connectivity failed\nWrite ../evaluate.json]
  C -- Yes --> D[Ensure key exists & chmod 0400 (best-effort)]
  D --> E{SSH connect OK?}
  E -- No --> F2[Record SSH Connectivity failed\nWrite ../evaluate.json]
  E -- Yes --> G{Docker daemon active?}
  G -- No --> H1[Record Docker Daemon Check failed\nMark Task1-4 as skipped\nWrite ../evaluate.json]
  G -- Yes --> T1_Start[Task1: Basic containers]

  %% Task1 sequence
  T1_Start --> T1A[Check lab1-hello\nexists, exited 0, logs contain hello, label lab=act1]
  T1A --> T1B[Check lab1-nginx\nrunning, host:8080->container:80, HTTP reachable, label lab=act1]
  T1B --> T1C[Check lab1-ubuntu\nrunning, /lab1.txt == \"ok\", label lab=act1]
  T1C --> AfterT1

  AfterT1 --> ReadAns{ans.json present & has keys?}
  ReadAns -- No --> F3[Task2: ans.json values failed\nTask3: non-root skipped\nWrite ../evaluate.json]
  ReadAns -- Yes --> T2[TASK2: Verify ans.json values\n(CreatedAt, size, sha256, PATH)]
  T2 --> T3[TASK3: Non-root checks\n(ubuntu-default-user, nonroot user/uid, nonroot-int permissions & label)]
  T3 --> T4[TASK4: Housekeeping\n(no dangling images)]

  %% After all tests write results
  T4 --> S[Write ../evaluate.json with results]
  F1 --> S
  F2 --> S
  H1 --> S
  F3 --> S
  S --> Z[End]

  %% Optional small notes (short labels only to keep compatibility)
  %% Use simple styling later in a renderer that supports classDef if desired.

```
