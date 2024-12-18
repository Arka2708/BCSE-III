import java.io.*;
import java.util.*;

class Job{
    public int id;
    public int priority;
    public int arrivalTime;
    public int completionTime;
    public List<Integer> cpuBursts;
    public List<Integer> ioBursts;
    public int totalCpuBurts;
    public int currentCpuBurstIndex;
    public int currentIoBurstIndex;
    private boolean isCompleted;
    private boolean isInCPU;

    public Job(int id, int priority, int arrivalTime, List<Integer> cpuBursts, List<Integer> ioBursts){
        this.id = id;  this.priority = priority;  this.arrivalTime = arrivalTime;
        this.completionTime = 0; this.cpuBursts = cpuBursts; this.ioBursts = ioBursts;
        this.currentCpuBurstIndex = 0; this.currentIoBurstIndex = 0;
        this.isCompleted = false; this.isInCPU = true;
        this.totalCpuBurts = cpuBursts.stream().reduce(0, (a,b)->a+b);
    }

    public static Job fromString(String txt){
        txt =  txt.strip();
        String[] parts = txt.split(" ");
        if(parts.length < 3){
            throw new IllegalArgumentException("Invalid job string");
        }
        int id = Integer.parseInt(parts[0]);
        int priority = Integer.parseInt(parts[1]);
        int arrivalTime = Integer.parseInt(parts[2]);
        List<Integer> cpuBursts = new ArrayList<>();
        List<Integer> ioBursts = new ArrayList<>();
        for(int i = 3; i < parts.length; i++){
            if((i-3)%2 == 0){
                cpuBursts.add(Integer.parseInt(parts[i]));
            }else{
                ioBursts.add(Integer.parseInt(parts[i]));
            }
        }
        return new Job(id, priority, arrivalTime, cpuBursts, ioBursts);
    }

    public String toString(){
        return String.format("Job %d: priority %d, arrival time %d, cpu bursts %s, io bursts %s", id, priority, arrivalTime, cpuBursts.toString(), ioBursts.toString());
    }
    public void decrementCPUBurstTime(){
        if(isCompleted) return;
        cpuBursts.set(currentCpuBurstIndex, cpuBursts.get(currentCpuBurstIndex)-1);
        if(cpuBursts.get(currentCpuBurstIndex) == 0){
            if(currentCpuBurstIndex >= cpuBursts.size()-1){
                isCompleted = true;
                isInCPU = false;
            }else{
                currentCpuBurstIndex++;
                isInCPU = false;
            }
        }
    }
    public void decrementIOBurstTime(){
        if(isCompleted) return;
        ioBursts.set(currentIoBurstIndex, ioBursts.get(currentIoBurstIndex)-1);
        if(ioBursts.get(currentIoBurstIndex) == 0){
            currentIoBurstIndex++;
            isInCPU = true;
        }
    }
    public boolean isProcessCompleted(){
        return isCompleted;
    }
    public boolean isInCPU(){
        return isInCPU;
    }
}

enum JobSchedulerType{
    NONE,
    PRIORITY,
    RR
}

class Pair<T1, T2>{
    public T1 first;
    public T2 second;
    public Pair(T1 first, T2 second){
        this.first = first;
        this.second = second;
    }
}

class JobScheduler{
    List<Job> jobs;
    boolean debug;
    JobSchedulerType type;
    int time;
    List<Pair<Pair<Integer, Integer>, Job>> ganttChart;
 // Constructor accepts a filename to import job profiles
    public JobScheduler(String filename, boolean debug){
        this.debug = debug;
        type = JobSchedulerType.NONE;
        time = 0;
        ganttChart = new ArrayList<>();
        jobs = new ArrayList<>();
        try{
            BufferedReader br = new BufferedReader(new FileReader(filename));
            String line = br.readLine();
            String[] jobsTxt = line.split("-1");
            for(String jobTxt : jobsTxt){
                try {
                    jobs.add(Job.fromString(jobTxt));
                } catch (Exception e) {}
            }
            br.close();
            System.out.println("Imported "+Integer.toString(jobs.size())+" profiles");
        }catch(Exception e){
            e.printStackTrace();
        }
        if(debug){
            System.out.println("----------- Imported Jobs ------------");
            for (Job job : jobs) {
                System.out.println(job);
            }
            System.out.println("-------------------------------------");
        }
    }
 // Function to set the job scheduler type
    public void setJobSchedulerType(JobSchedulerType type){
        this.type = type;
    }
    // Function to check if all jobs completed
    private boolean isAllJobsCompleted(){
        for (Job job : jobs) {
            if(job.isProcessCompleted() == false) return false;
        }
        return true;
    }
   // Function to run the job scheduler
    public void run(){
        if(type == JobSchedulerType.NONE){
            System.out.println("No job scheduler type set");
            return;
        }
        if(jobs.size() == 0){
            System.out.println("No jobs to schedule");
            return;
        }
        switch(type){
            case PRIORITY:
                runPriority();
                break;
            case RR:
                runRr();
                break;
            default:
                System.out.println("Invalid job scheduler type");
                break;
        }                                                                                                                                                               
    }
    // Function to run the priority job scheduler
    private void runPriority(){
        // Priority with preemptive
        System.out.println("\nRunning Priority job scheduler .. .. .. ");
        // Sort all the processes according to arrrival time
        Collections.sort(this.jobs, new Comparator<Job>() {
            @Override
            public int compare(Job o1, Job o2) {
                return o1.arrivalTime - o2.arrivalTime;
            }
        });
        PriorityQueue<Job> readyProcessesQueue = new PriorityQueue<Job>(new Comparator<Job>() {
            @Override
            public int compare(Job o1, Job o2) {
                return o1.priority - o2.priority;
            }
        });

        List<Job> blockProcesses = new ArrayList<>();
        Job currentJob;

        while(isAllJobsCompleted() == false){
            // Add processes to ready queue
            for(Job job: jobs){
                if(job.arrivalTime == time){
                    readyProcessesQueue.add(job);
                }
            }
            List<Job> tempBlockProcesses = new ArrayList<>();
            tempBlockProcesses.addAll(blockProcesses);

            // Check if there is any process in ready queue
            if(readyProcessesQueue.size() != 0){          
                // Get the first process from the ready queue
                currentJob = readyProcessesQueue.peek();
                currentJob.decrementCPUBurstTime();
                // Add the process to gantt chart
                ganttChart.add(new Pair<>(new Pair<>(time, time+1), currentJob));
                if(!currentJob.isInCPU()){
                    // If the process is not in CPU, add it to block list            
                    if(currentJob.isProcessCompleted()){
                        currentJob.completionTime = time+1;
                        // If the process has been completed then remove from the ready queue
                        readyProcessesQueue.remove(currentJob);
                    }else{
                        // If the current job is not in CPU, it means it is in IO burst, So move it to block queue
                        readyProcessesQueue.remove(currentJob);
                        blockProcesses.add(currentJob);
                    }
                }
            }
            // Do the IO burst for all the processes in block queue
            for(Job job : tempBlockProcesses){
                job.decrementIOBurstTime();
                if(job.isInCPU()){
                    // If the current job is in CPU, it means it is out of IO burst, So move it to ready queue
                    blockProcesses.remove(job);
                    readyProcessesQueue.add(job);
                }
            }
            time +=1;
        }
    }
   // Function to run the round robin job scheduler
    private void runRr(){
        System.out.println("\nRunning Round Robin job scheduler .. .. ..");
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the time quantum: ");
        int timeQuantum = sc.nextInt();
        // Sort all the processes according to arrrival time
        Collections.sort(this.jobs, new Comparator<Job>() {
            @Override
            public int compare(Job o1, Job o2) {
                return o1.arrivalTime - o2.arrivalTime;
            }
        });
        if(debug){
            for(Job job : jobs){
                System.out.println(job);
            }
        }
        Job currentJob ;
        Queue<Job> readyProcessesQueue = new LinkedList<>();
        List<Job> blockProcesses = new ArrayList<>();
        int timeQuantumCounter = 0;
        while(isAllJobsCompleted() == false){
            // Add processes to ready queue
            for(Job job: jobs){
                if(job.arrivalTime == time){
                    readyProcessesQueue.add(job);
                }
            }
            List<Job> tempBlockProcesses = new ArrayList<>();
            tempBlockProcesses.addAll(blockProcesses);
            // Check if there is any process in ready queue
            if(readyProcessesQueue.size() != 0){            
                if(timeQuantumCounter == timeQuantum){
                    // If the time quantum is completed, move the current process to the end of the queue
                    readyProcessesQueue.add(readyProcessesQueue.poll());
                    timeQuantumCounter = 0;
                }
                // Get the first process from the ready queue
                currentJob = readyProcessesQueue.peek();
                currentJob.decrementCPUBurstTime();
                // Add the process to gantt chart
                ganttChart.add(new Pair<>(new Pair<>(time, time+1), currentJob));            
                if(!currentJob.isInCPU()){
                    // If the process is not in CPU, add it to block list              
                    if(currentJob.isProcessCompleted()){
                        currentJob.completionTime = time+1;
                        // If the process has been completed then remove from the ready queue
                        readyProcessesQueue.poll();
                    }else{
                        // If the current job is not in CPU, it means it is in IO burst, So move it to block queue
                        readyProcessesQueue.poll();
                        blockProcesses.add(currentJob);
                    }
                }
            }
            // Do the IO burst for all the processes in block queue
            for(Job job : tempBlockProcesses){
                job.decrementIOBurstTime();
                if(job.isInCPU()){
                    // If the current job is in CPU, it means it is out of IO burst, So move it to ready queue
                    blockProcesses.remove(job);
                    readyProcessesQueue.add(job);
                }
            }
            time+=1;
            timeQuantumCounter+=1;
        }
    }
    // Function to print gantt chart
    public void printGanttChart(){
        System.out.println("------------------\nFinal Gantt Chart\n------------------");
        for (Pair<Pair<Integer, Integer>, Job> pair : ganttChart) {
            System.out.println("Time: "+pair.first.first+"-"+pair.first.second+"\tJob: "+pair.second.id);
        }
    }   
    // Function to calculate the stats
    public void calculateStats(){
        int waitingTime = 0;
        int turnaroundTime = 0;
        int totalCpuBursts = 0;
        for (Job job : jobs) {
            turnaroundTime += (job.completionTime - job.arrivalTime);
            waitingTime += (job.completionTime - job.arrivalTime - job.totalCpuBurts);
            totalCpuBursts += job.totalCpuBurts;
        }
        System.out.println("\n-- Stats --");
        System.out.println("Average waiting time: "+((waitingTime*1.0)/jobs.size()));
        System.out.println("Average turnaround time: "+((turnaroundTime*1.0)/jobs.size()));
        System.out.println("CPU Utilization: "+Math.round((totalCpuBursts*1.0)/time * 100)+" %");
    }
}

public class q8 {
    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        int choice = 0;
        JobScheduler jobScheduler = null;
        do{
            System.out.println("\n\n");
            System.out.println("1. Schedule jobs using Priority Scheduling Preamptive");
            System.out.println("2. Schedule jobs using RR");
            System.out.println("3. Exit");
            System.out.print("Enter your choice : ");
            choice = sc.nextInt();
            sc.nextLine();
            if(choice!=3){
            System.out.print("Enter the filename: ");
            String filename2 = sc.nextLine();
            jobScheduler = new JobScheduler(filename2, false);
            }
            switch(choice){
                case 1:
                    jobScheduler.setJobSchedulerType(JobSchedulerType.PRIORITY);
                    jobScheduler.run();
                    jobScheduler.printGanttChart();
                    jobScheduler.calculateStats();
                    break;
                case 2:
                    jobScheduler.setJobSchedulerType(JobSchedulerType.RR);
                    jobScheduler.run();
                    jobScheduler.printGanttChart();
                    jobScheduler.calculateStats();
                    break;
                case 3:
                    System.out.println("Exiting .. .. ..");
                    break;
                default:
                    System.out.println("Invalid choice");
            }
        }while(choice != 3);
    }
}