function Sensors=disToSink(Sensors,Model)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

    n=Model.n;
    for i=1:n
        
        distance=sqrt((Sensors(i).xd-Sensors(n+1).xd)^2 + ...
            (Sensors(i).yd-Sensors(n+1).yd)^2 );
        
        Sensors(i).dis2sink=distance;
        
    end
    
end