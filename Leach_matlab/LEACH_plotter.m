function deadNum=LEACH_plotter(Sensors,Model)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

    deadNum=0;
    n=Model.n;
    for i=1:n
        %check dead node
        if (Sensors(i).E>0)
            
            if(Sensors(i).type=='N' )      
                % text(Sensors(i).xd+1,Sensors(i).yd-1,num2str(i));
                % plot(Sensors(i).xd,Sensors(i).yd,'o');
                plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'k');
            else %Sensors.type=='C'       
                %  text(Sensors(i).xd+1,Sensors(i).yd-1,num2str(i));
                % plot(Sensors(i).xd,Sensors(i).yd,'kx','MarkerSize',10);
                plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'r');
            end
            
        else
            deadNum=deadNum+1;
            % plot(Sensors(i).xd,Sensors(i).yd,'red .');
            % text(Sensors(i).xd+1,Sensors(i).yd-1,num2str(i));
            plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
        end
        
        hold on;
        
    end 
    % plot(Sensors(n+1).xd,Sensors(n+1).yd,'g*','MarkerSize',15);
    
    plot(Sensors(n+1).xd,Sensors(n+1).yd,'bo', 'MarkerSize', 8, 'MarkerFaceColor', 'b');
    text(Sensors(n+1).xd+1,Sensors(n+1).yd-1,'Sink');
    axis square

end