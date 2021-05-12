function Sensors=joinToNearestCH(Sensors,Model,TotalCH)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

n=Model.n;
m=length(TotalCH);
if(m>1)
    D=zeros(m,n);  
    for i=1:n     
        for j=1:m
            
            D(j,i)=sqrt((Sensors(i).xd-Sensors(TotalCH(j).id).xd)^2+ ...
                (Sensors(i).yd-Sensors(TotalCH(j).id).yd)^2);        
        end   
    end 
    
    %% 
    [Dmin,idx]=min(D);
    
    for i=1:n       
        if (Sensors(i).E>0)
            %if node is in RR CH and is Nearer to CH rather than Sink
            if (Dmin(i) <= Model.RR && Dmin(i)<Sensors(i).dis2sink )
                Sensors(i).MCH=TotalCH(idx(i)).id;
                Sensors(i).dis2ch=Dmin(i);
            else
                Sensors(i).MCH=n+1;
                Sensors(i).dis2ch=Sensors(i).dis2sink;
            end
        end
        
    end 
end

end

