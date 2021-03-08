from math import *
from Base_modules.LEACH_setParameters import *
from Base_modules.LEACH_configureSensors import *


# function Sender=findSender(Sensors,Model,Receiver)
# %% Standard Leach Developed by Amin Nazari
# %   aminnazari91@gmail.com
# %   0918 546 2272
# %% Improved Leach Developed by Hritwik Singhal and Nishita Agarwal
#
#     Sender=[];
#
#     n=Model.n;
#
#     for i=1:n
#
#         if (Sensors(i).MCH==Receiver & Sensors(i).id~=Receiver)
#             Sender=[Sender,Sensors(i).id]; %#ok
#         end
#
#     end
#
# end

def start(Sensors: list[Sensor], myModel: Model, Receivers):
    pass
