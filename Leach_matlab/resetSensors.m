function Sensors=resetSensors(Sensors,Model)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

    n=Model.n;
    for i=1:n
        Sensors(i).MCH=n+1;
        Sensors(i).type='N';
        Sensors(i).dis2ch=inf;
    end
    
end