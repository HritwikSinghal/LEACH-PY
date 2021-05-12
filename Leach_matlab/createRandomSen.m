function createRandomSen(Model,Area)
%% Standard Leach Developed by Amin Nazari 
%   aminnazari91@gmail.com 
%   0918 546 2272
%% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal 

    n=Model.n;
    x=Area.x;
    y=Area.y;
    X=zeros(1,n);
    Y=X;
    for i=1:1:n
        X(i)=rand()*x;
        Y(i)=rand()*y;
    end
    save ('Locations','X','Y');

end