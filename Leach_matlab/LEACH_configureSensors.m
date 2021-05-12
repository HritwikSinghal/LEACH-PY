function Sensors=LEACH_configureSensors(Model,n,GX,GY)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

%% Configuration EmptySensor
EmptySensor.xd=0;
EmptySensor.yd=0;
EmptySensor.G=0;
EmptySensor.df=0;
EmptySensor.type='N';
EmptySensor.E=0; 
EmptySensor.id=0;
EmptySensor.dis2sink=0;
EmptySensor.dis2ch=0;
EmptySensor.MCH=n+1;    %Member of CH

%% Configuration Sensors
Sensors=repmat(EmptySensor,n+1,1);

for i=1:1:n
    %set x location
    Sensors(i).xd=GX(i); 
    %set y location
    Sensors(i).yd=GY(i);
    %Determinate whether in previous periods has been clusterhead or not? not=0 and be=n
    Sensors(i).G=0;
    %dead flag. Whether dead or alive S(i).df=0 alive. S(i).df=1 dead.
    Sensors(i).df=0; 
    %initially there are not each cluster heads 
    Sensors(i).type='N';
    %initially all nodes have equal Energy
    Sensors(i).E=Model.Eo;
    %id
    Sensors(i).id=i;
    %Sensors(i).RR=Model.RR;
    
end 

Sensors(n+1).xd=Model.Sinkx; 
Sensors(n+1).yd=Model.Sinky;
Sensors(n+1).E=100;
Sensors(n+1).id=n+1;
end