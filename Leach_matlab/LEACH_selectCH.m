function [CH,Sensors]=LEACH_selectCH(Sensors,Model,r)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

    CH=[];
    countCHs=0;
    n=Model.n;
    
    for i=1:1:n
        if(Sensors(i).E>0)          
            temp_rand=rand;     
            if (Sensors(i).G<=0)            
                %Election of Cluster Heads
                if(temp_rand<= (Model.p/(1-Model.p*mod(r,round(1/Model.p)))))                    
                    countCHs=countCHs+1; 
                    CH(countCHs).id=i; %#ok                
                    Sensors(i).type='C';
                    Sensors(i).G=round(1/Model.p)-1;        
                end    
            end   
        end 
    end 
end
