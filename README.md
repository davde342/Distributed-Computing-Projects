# Distributed Computing Assignments

This repository contains two assignments for the Distributed Computing course. Both assignments focus on extending baseline simulation models (a queueing simulator and a peer-to-peer backup simulator) to test new architectural questions and hypotheses.

---

## 🏗️ First Assignment: Queueing Simulator Extension

**Location:** `first_assignment/`

### Overview
This assignment explores an extension to a queueing simulator by answering the following question: 
> *"If we add the functionalities of a dynamic-D and job stealing to our simulator, can we obtain a system that performs better than the original one?"*

### Key Features
1. **Dynamic-D Load Balancing:** The original system uses a fixed $D$ (number of queues sampled to assign a new job). The extension dynamically adjusts $D$ based on the Coefficient of Variation ($CV = \frac{\text{Standard Deviation}}{\text{Average Load of Queues}}$). If the system is highly unbalanced ($CV \ge 1$), $D$ is increased to sample more queues and find an optimal destination. We implemented and evaluated 5 different Dynamic-D algorithms.
2. **Job Stealing:** When a job is completed and its queue is empty, the server steals half of the jobs from the most loaded queue among a set of $D$ sampled servers. 

### Conclusions
- **Under High Workload ($\lambda = 0.99$):** The system benefits significantly from Dynamic-D and job stealing. The queues tend to be unbalanced, so dynamicity and stealing effectively reduce waiting times.
- **Under Low Workload ($\lambda = 0.5$):** The original approach with fixed $D = N/2$ performs better. Queues are mostly balanced, making the overhead of dynamic-D and Job Stealing unnecessary.
- **Scalability:** By increasing the total number of servers, the average queue length decreases naturally, meaning the original baseline system easily outperforms the dynamic methods as the system scales.

---

## 💾 Second Assignment: P2P Backup Simulator Extension

**Location:** `second_assignment/`

### Overview
This assignment extends a P2P storage/backup simulator (`storage.py`) by introducing different priority classes for peers. The question answered is: 
> *"If we add high-priority peers to the system, which have to store and backup faster than low-priority peers, what will be the impact on the overall network?"*

### Key Features
1. **High Priority Peers:** A designated percentage of peers is assigned high priority status.
2. **Dynamic Backup/Restore Thresholds:** We introduced configurable threshold percentages (`PER_BACKUP` and `PER_RESTORE`) linked to the global pool of high-priority blocks. 
   - A low-priority node cannot perform a backup if the global fraction of successfully backed up high-priority blocks is lower than `PER_BACKUP`.
   - A low-priority node cannot perform a restore if the current proportion of high-priority blocks still needing restore exceeds `PER_RESTORE`.
3. **Data Loss Tracking:** The simulator tracks blocks lost due to node failures and assesses data loss rates for both priority classes independently.


## 🚀 Execution and Outputs

Inside each respective folder (`first_assignment` and `second_assignment`), you will find the `README` files with specific commands and details on the plotting scripts generated to analyze and visualize the results (e.g., job completion times, probability plots of queue tails, percentage of average backed up blocks vs years, etc.).

*Authors: Francesco Matano & Davide Giusto*
