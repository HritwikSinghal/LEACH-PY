function [Area,Model]=LEACH_setParameters(n)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

%%%%%%%%%%%%%%%%%%%%%%%%% Set Inital PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%
%Field Dimensions - x and y maximum (in meters)
Area.x=1000;
Area.y=1000;

%Sink Motion pattern 
Sinkx=0.5*Area.x;
Sinky=Sinkx;

%Optimal Election Probability of a node to become cluster head
p=0.1;

%%%%%%%%%%%%%%%%%%%%%%%%% Energy Model (all values in Joules)%%%%%%%%%%%
%Initial Energy 
Eo=2;

%Eelec=Etx=Erx
ETX=50*0.000000001;
ERX=50*0.000000001;

%Transmit Amplifier types
Efs=10e-12;
Emp=0.0013*0.000000000001;

%Data Aggregation Energy
EDA=5*0.000000001;

%Computation of do
do=sqrt(Efs/Emp);

%%%%%%%%%%%%%%%%%%%%%%%%% Run Time Parameters %%%%%%%%%%%%%%%%%%%%%%%%%
%maximum number of rounds
rmax=400;

%Data packet size
DpacketLen=4000;

%Hello packet size
HpacketLen=100;

%Number of Packets sended in steady-state phase
NumPacket=10;

%Radio Range
RR=0.5*Area.x*sqrt(2);
%%%%%%%%%%%%%%%%%%%%%%%%% END OF PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%% Save in Model %%%%%%%%%%%%%%%%%%%%%%%%%%%%
Model.n=n;
Model.Sinkx=Sinkx;
Model.Sinky=Sinky;
Model.p=p;
Model.Eo=Eo;
Model.ETX=ETX;
Model.ERX=ERX;
Model.Efs=Efs;
Model.Emp=Emp;
Model.EDA=EDA;
Model.do=do;
Model.rmax=rmax;
Model.DpacketLen=DpacketLen;
Model.HpacketLen=HpacketLen;
Model.NumPacket=NumPacket;
Model.RR=RR;

end