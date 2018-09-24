# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 11:11:35 2018

@author: PLJAOTT
"""

import numpy as np
#import BullyPool as BP


def SimplePoolAI(Player, ColorAssignment, MaxStrokePower, UnpottedBalls, Break, ReadyForTheBlack, BallLocationX, BallLocationY, PoolParams, pocket_positions):
    
    StrokeAngle = 0;
    
    
    if Break == 1:
        CueBallDistToObjectBallX = BallLocationX[UnpottedBalls[1]] - BallLocationX[0];
        CueBallDistToObjectBallY = BallLocationY[UnpottedBalls[1]] - BallLocationY[0];
        CueBallDistToObjectBall = np.sqrt((CueBallDistToObjectBallX**2) + (CueBallDistToObjectBallY**2))
        CueBallAngleToObjectBall = np.angle(CueBallDistToObjectBallX + 1j*CueBallDistToObjectBallY);
        CueToObjectAngleThreshold = np.abs(np.arcsin(PoolParams['BallDiameter']/(2*CueBallDistToObjectBall)));
        StrokeSpeed = MaxStrokePower
        StrokeAngle = CueBallAngleToObjectBall+ np.random.uniform(-1, 1) * CueToObjectAngleThreshold;
    else:
        
        PocketLocations = np.zeros([6,2])
        cnt = 0;
        for key, pocket in pocket_positions.items():
            if 'Top' in key:
                PocketLocations[cnt,1] = pocket[1]-(PoolParams['BallDiameter']/2)
            else:
                PocketLocations[cnt,1] = pocket[1]+(PoolParams['BallDiameter'])
            
            if 'Left' in key:
                PocketLocations[cnt,0] = pocket[0]+(PoolParams['BallDiameter'])
            elif 'Right' in key:
                PocketLocations[cnt,0] = pocket[0]-(PoolParams['BallDiameter'])
            else:
                if BallLocationX[0] > pocket[0]+(PoolParams['BallDiameter']):
                    PocketLocations[cnt,0] = pocket[0]-(PoolParams['BallDiameter'])
                elif BallLocationX[0] < pocket[0]-(PoolParams['BallDiameter']):
                    PocketLocations[cnt,0] = pocket[0]+(PoolParams['BallDiameter'])
                else:
                    PocketLocations[cnt,0] = pocket[0]
            
            cnt = cnt+1
#        PocketLocations = np.array([[0, 0],
#                                    [0, PoolParams['TableWidth']],
#                                    [PoolParams['TableLength']/2, PoolParams['BallDiameter']/2],
#                                    [PoolParams['TableLength']/2, PoolParams['TableWidth']-PoolParams['BallDiameter']/2],
#                                    [PoolParams['TableLength'],0],
#                                    [PoolParams['TableLength'], PoolParams['TableWidth']]])
        
    
        (MaxEaseOfStroke, BallToAimFor, AngleToPocket) = EstimateEaseOfStroke(UnpottedBalls, 
        Player, ColorAssignment, ReadyForTheBlack, BallLocationX, BallLocationY, PoolParams, PocketLocations)
        if MaxEaseOfStroke == 0:
            # Snookered
            StrokeAngle = GetOutOfSnooker(UnpottedBalls, Player, ColorAssignment, ReadyForTheBlack, 
                                          BallLocationX, BallLocationY, PoolParams, PocketLocations)
        
        else:
          
        
            DesiredImpactLocationX = BallLocationX[BallToAimFor] - PoolParams['BallDiameter']*np.cos(AngleToPocket);
            DesiredImpactLocationY = BallLocationY[BallToAimFor] - PoolParams['BallDiameter']*np.sin(AngleToPocket);
            
            CueBallDistToDesiredImpactLocationX = DesiredImpactLocationX - BallLocationX[0];
            CueBallDistToDesiredImpactLocationY = DesiredImpactLocationY - BallLocationY[0];
            
            StrokeAngle = np.angle(CueBallDistToDesiredImpactLocationX + 1j*CueBallDistToDesiredImpactLocationY);
    
    
        StrokeSpeed = MaxStrokePower;
           
    
    return(StrokeSpeed, StrokeAngle)
    
    
    
def OneLookAheadPoolAI(Player, ColorAssignment, MaxStrokePower, UnpottedBalls, Break, ReadyForTheBlack, BallLocationX, BallLocationY, PoolParams, Ball, PoolFigure, PoolTableAxes, NoSpeedsToTest):
    
    
    PlotAnimation = 0;
    StrokeAngle = 0;
    
    
    if Break == 1:
        CueBallDistToObjectBallX = BallLocationX[UnpottedBalls[1]] - BallLocationX[0];
        CueBallDistToObjectBallY = BallLocationY[UnpottedBalls[1]] - BallLocationY[0];
        CueBallDistToObjectBall = np.sqrt((CueBallDistToObjectBallX**2) + (CueBallDistToObjectBallY**2))
        CueBallAngleToObjectBall = np.angle(CueBallDistToObjectBallX + 1j*CueBallDistToObjectBallY);
        CueToObjectAngleThreshold = np.abs(np.arcsin(PoolParams['BallDiameter']/(2*CueBallDistToObjectBall)));
        OptimumStrokeSpeed = MaxStrokePower;
        StrokeAngle = CueBallAngleToObjectBall + np.random.uniform(-0.5, 0.5) * CueToObjectAngleThreshold;
    else:
        
    
#        PocketLocations = np.array([[0, 0],
#                                    [0, PoolParams['TableWidth']],
#                                    [PoolParams['TableLength']/2, 0],
#                                    [PoolParams['TableLength']/2, PoolParams['TableWidth']-0],
#                                    [PoolParams['TableLength'],0],
#                                    [PoolParams['TableLength'], PoolParams['TableWidth']]])
        
        PocketLocations = np.zeros([6,2])
        cnt = 0;
        for key, pocket in pocket_positions.items():
            if 'Top' in key:
                PocketLocations[cnt,1] = pocket[1]-(PoolParams['BallDiameter']/2)
            else:
                PocketLocations[cnt,1] = pocket[1]+(PoolParams['BallDiameter']/2)
            
            if 'Left' in key:
                PocketLocations[cnt,0] = pocket[0]+(PoolParams['BallDiameter']/2)
            elif 'Right' in key:
                PocketLocations[cnt,0] = pocket[0]-(PoolParams['BallDiameter']/2)
            else:
                if BallLocationX[0] > pocket[0]+(PoolParams['BallDiameter']/2):
                    PocketLocations[cnt,0] = pocket[0]-(PoolParams['BallDiameter']/2)
                elif BallLocationX[0] < pocket[0]-(PoolParams['BallDiameter']/2):
                    PocketLocations[cnt,0] = pocket[0]+(PoolParams['BallDiameter']/2)
                else:
                    PocketLocations[cnt,0] = pocket[0]
            
            cnt = cnt+1
        
        OptimumStrokeSpeed = MaxStrokePower;
        
    #    PotDifficulty = np.zeros((len(UnpottedBalls)-1,len(PocketLocations)))
        
    #    Player
    #    if ColorAssignment[Player-1] == 1:
        
        (MaxEaseOfStroke, BallToAimFor, AngleToPocket) = EstimateEaseOfStroke(UnpottedBalls, Player, 
        ColorAssignment, ReadyForTheBlack, BallLocationX, 
        BallLocationY, PoolParams,
        PocketLocations)
        
        if MaxEaseOfStroke == 0:
            # Snookered
            StrokeAngle = GetOutOfSnooker(UnpottedBalls, Player, ColorAssignment, 
                                          ReadyForTheBlack, BallLocationX, BallLocationY, 
                                          PoolParams, PocketLocations)
        
        else:
                
            DesiredImpactLocationX = BallLocationX[BallToAimFor] - PoolParams['BallDiameter']*np.cos(AngleToPocket);
            DesiredImpactLocationY = BallLocationY[BallToAimFor] - PoolParams['BallDiameter']*np.sin(AngleToPocket);
            
            CueBallDistToDesiredImpactLocationX = DesiredImpactLocationX - BallLocationX[0];
            CueBallDistToDesiredImpactLocationY = DesiredImpactLocationY - BallLocationY[0];
            
            StrokeAngle = np.angle(CueBallDistToDesiredImpactLocationX + 1j*CueBallDistToDesiredImpactLocationY);
    
    
        
        
        PlotAnimation = 0
        MaxEaseOfNextStroke = 0
        MinOpponentEaseOfNextStroke = 9999
        
        
        for I in range(1,NoSpeedsToTest):
            StrokeSpeed = (NoSpeedsToTest-I)*MaxStrokePower/NoSpeedsToTest
            NewBallLocationX = BallLocationX
            NewBallLocationY = BallLocationY
            NewBall = Ball
            NewUnpottedBalls = list(UnpottedBalls)
            NewReadyForTheBlack = list(ReadyForTheBlack)
            NewPoolFigure = PoolFigure
            NewPoolTableAxes = PoolTableAxes
            
            (NewBallLocationX, NewBallLocationY, NewBall, NewFirstBallBallContact, NewPotCount,
             NewBallPotSeq, NewUnpottedBalls, NewPoolFigure) = BP.Pool_PlayShot(StrokeSpeed,
                                                           StrokeAngle, BallLocationX, BallLocationY,
                                                           PoolParams, NewUnpottedBalls, PlotAnimation,
                                                           NewBall, NewPoolFigure, NewPoolTableAxes)
            
            
            (NewFoul, NewReadyForTheBlack, NewEndofGame, NewColorAssignment,
             NewPlayer, NewUnpottedBalls, NewBallLocationX, NewBallLocationY, PoolMsg) = BP.Pool_Rules(NewReadyForTheBlack,
                                                                                     ColorAssignment, NewFirstBallBallContact,
                                                                                     Player, NewPotCount, NewBallPotSeq, 
                                                                                     NewUnpottedBalls, NewBallLocationX,NewBallLocationY, 
                                                                                     PoolParams)
            
            
            if NewFoul == 0:
                (EaseOfNextStroke, NextBallToAimFor, NextAngleToPocket) = EstimateEaseOfStroke(NewUnpottedBalls, 
                NewPlayer, NewColorAssignment, NewReadyForTheBlack, NewBallLocationX, NewBallLocationY, PoolParams, PocketLocations)
                    
                if NewPlayer == Player:
                    if EaseOfNextStroke > MaxEaseOfNextStroke:
                        MaxEaseOfNextStroke = EaseOfNextStroke
                        OptimumStrokeSpeed = StrokeSpeed
                else:
                    if EaseOfNextStroke < MinOpponentEaseOfNextStroke:
                        MinOpponentEaseOfNextStroke = EaseOfNextStroke
                        if MaxEaseOfNextStroke == 0:
                            OptimumStrokeSpeed = StrokeSpeed
            
    
    return(OptimumStrokeSpeed, StrokeAngle)
    
    
def EstimateEaseOfStroke(UnpottedBalls, Player, ColorAssignment, ReadyForTheBlack, 
                         BallLocationX, BallLocationY, PoolParams, PocketLocations):
    MaxEaseOfStroke = 0;
    if ReadyForTheBlack[Player-1] == 1:
        BallToAimFor = 8
    else:
        BallToAimFor = UnpottedBalls[1]
    
    AngleToPocket = 0;
        
    if ReadyForTheBlack[Player-1] == 0:
        CannotStrikeBlack = 1;
    else:
        CannotStrikeBlack = 0;
    
    CueBallDistToObjectBall = np.zeros(len(UnpottedBalls))
    CueBallAngleToObjectBall = np.zeros(len(UnpottedBalls))
    CueToObjectAngleThreshold = np.zeros(len(UnpottedBalls))
    
    ObjectBallDistToPocket = np.zeros((len(UnpottedBalls),len(PocketLocations)))
    ObjectBallAngleToPocket = np.zeros((len(UnpottedBalls),len(PocketLocations)))
        
    for I in range(1,len(UnpottedBalls)):
        CueBallDistToObjectBallX = BallLocationX[UnpottedBalls[I]] - BallLocationX[0];
        CueBallDistToObjectBallY = BallLocationY[UnpottedBalls[I]] - BallLocationY[0];
        CueBallDistToObjectBall[I] = np.sqrt((CueBallDistToObjectBallX**2) + (CueBallDistToObjectBallY**2))
        CueBallAngleToObjectBall[I] = np.angle(CueBallDistToObjectBallX + 1j*CueBallDistToObjectBallY);
        CueToObjectAngleThreshold[I] = np.abs(np.arcsin(PoolParams['BallDiameter']/CueBallDistToObjectBall[I]));
        
        for J in range(0,len(PocketLocations)):  
            ObjectBallDistToPocketX = PocketLocations[J,0] -  BallLocationX[UnpottedBalls[I]];
            ObjectBallDistToPocketY = PocketLocations[J,1] -  BallLocationY[UnpottedBalls[I]];
            ObjectBallDistToPocket[I,J] = np.sqrt((ObjectBallDistToPocketX**2) + (ObjectBallDistToPocketY**2))
            ObjectBallAngleToPocket[I,J] = np.angle(ObjectBallDistToPocketX + 1j*ObjectBallDistToPocketY);
        
    OrderedCueBallDistToObjectBall = np.argsort(CueBallDistToObjectBall)
    
    for I in range(1,len(UnpottedBalls)):
        if (ColorAssignment[Player-1] == 0) | ((ColorAssignment[Player-1] == 1)
        & (UnpottedBalls[I] < (9-CannotStrikeBlack))) | ((ColorAssignment[Player-1] == 2) 
        & (UnpottedBalls[I] > (7+CannotStrikeBlack))):
            for J in range(0,len(PocketLocations)):     
                           
                CuttingAngle = ObjectBallAngleToPocket[I,J] - CueBallAngleToObjectBall[I];
                
                EaseOfStroke = (np.cos(CuttingAngle)/(ObjectBallDistToPocket[I,J]*CueBallDistToObjectBall[I]))
                
                DesiredImpactLocationX = BallLocationX[UnpottedBalls[I]] - PoolParams['BallDiameter']*np.cos(ObjectBallAngleToPocket[I,J]);
                DesiredImpactLocationY = BallLocationY[UnpottedBalls[I]] - PoolParams['BallDiameter']*np.sin(ObjectBallAngleToPocket[I,J]);
    
                CueBallDistToDesiredImpactLocationX = DesiredImpactLocationX - BallLocationX[0];
                CueBallDistToDesiredImpactLocationY = DesiredImpactLocationY - BallLocationY[0];
    
                StrokeAngle = np.angle(CueBallDistToDesiredImpactLocationX + 1j*CueBallDistToDesiredImpactLocationY);
                
                for K in range(1,len(OrderedCueBallDistToObjectBall)):
                    if OrderedCueBallDistToObjectBall[K] == I:
                        break
                    elif (StrokeAngle > CueBallAngleToObjectBall[OrderedCueBallDistToObjectBall[K]] - CueToObjectAngleThreshold[OrderedCueBallDistToObjectBall[K]]) & (StrokeAngle < CueBallAngleToObjectBall[OrderedCueBallDistToObjectBall[K]] + CueToObjectAngleThreshold[OrderedCueBallDistToObjectBall[K]]):
                        EaseOfStroke = 0;

                
                for K in range(1,len(UnpottedBalls)):
                    if UnpottedBalls[K] != UnpottedBalls[I]:
                        if ObjectBallDistToPocket[K,J] < ObjectBallDistToPocket[I,J]:
                            ObjectBallDistToObjectBallX = BallLocationX[UnpottedBalls[K]] -  BallLocationX[UnpottedBalls[I]];
                            ObjectBallDistToObjectBallY = BallLocationY[UnpottedBalls[K]] -  BallLocationY[UnpottedBalls[I]];
                            ObjectBallDistToObjectBall = np.sqrt((ObjectBallDistToObjectBallX**2) + (ObjectBallDistToObjectBallY**2))
                            ObjectBallAngleToObjectBall = np.angle(ObjectBallDistToObjectBallX + 1j*ObjectBallDistToObjectBallY);
                            ObjBallObjBallAngleThreshold = np.abs(np.arcsin(PoolParams['BallDiameter']/ObjectBallDistToObjectBall));
                            if (ObjectBallAngleToPocket[I,J] > ObjectBallAngleToObjectBall - ObjBallObjBallAngleThreshold) & (ObjectBallAngleToPocket[I,J] < ObjectBallAngleToObjectBall + ObjBallObjBallAngleThreshold):
                                EaseOfStroke = EaseOfStroke/10;
#                
                if EaseOfStroke > MaxEaseOfStroke:
                    MaxEaseOfStroke = EaseOfStroke
                    BallToAimFor = UnpottedBalls[I]
                    AngleToPocket = ObjectBallAngleToPocket[I,J];
    
    return(MaxEaseOfStroke, BallToAimFor, AngleToPocket)
    
    

def GetOutOfSnooker(UnpottedBalls, Player, ColorAssignment, ReadyForTheBlack, BallLocationX, BallLocationY, PoolParams, PocketLocations):
    
    
    if ReadyForTheBlack[Player-1] == 0:
        CannotStrikeBlack = 1;
    else:
        CannotStrikeBlack = 0;
            
    
    NoAnglesToTry = 1000
    MaxNoCushionSafety = 10
    
    TotalTravelDistance = np.zeros((1,NoAnglesToTry-1))
    BallStruck = np.zeros((1,NoAnglesToTry-1))
    NoCushions = np.zeros((1,NoAnglesToTry-1))
    
    for I in range(1,NoAnglesToTry):
        
        CueBallAngle = 2*np.pi *I/NoAnglesToTry +0.001 - np.pi
        CurrentCueBallLocationX = BallLocationX[0]
        CurrentCueBallLocationY = BallLocationY[0]
        
        for J in range(0,MaxNoCushionSafety):         
            

            
            if np.sin(CueBallAngle) > 0 :
                FirstYImpact = (PoolParams['TableWidth'] - CurrentCueBallLocationY - PoolParams['BallDiameter']/2)/np.sin(CueBallAngle)
                FirstYImpact = np.abs(FirstYImpact)
                NextCueBallLocationY_Y = (PoolParams['TableWidth'] - PoolParams['BallDiameter']/2)
                NextCueBallLocationY_X = CurrentCueBallLocationX + (PoolParams['TableWidth'] - CurrentCueBallLocationY - PoolParams['BallDiameter']/2)/np.tan(CueBallAngle)
                NextCueBallAngleY = np.angle(NextCueBallLocationY_X - CurrentCueBallLocationX - 1j*(PoolParams['TableWidth'] - CurrentCueBallLocationY - PoolParams['BallDiameter']/2));
            elif np.sin(CueBallAngle) < 0 :
                FirstYImpact = (CurrentCueBallLocationY- PoolParams['BallDiameter']/2)/np.sin(CueBallAngle)
                FirstYImpact = np.abs(FirstYImpact)
                NextCueBallLocationY_Y = (PoolParams['BallDiameter']/2)
                NextCueBallLocationY_X = CurrentCueBallLocationX - (CurrentCueBallLocationY- PoolParams['BallDiameter']/2)/np.tan(CueBallAngle)
                NextCueBallAngleY = np.angle(NextCueBallLocationY_X - CurrentCueBallLocationX + 1j*(CurrentCueBallLocationY- PoolParams['BallDiameter']/2));
            else:
                FirstYImpact = 9999

            if np.cos(CueBallAngle) > 0 :
                FirstXImpact = (PoolParams['TableLength'] - CurrentCueBallLocationX- PoolParams['BallDiameter']/2)/np.cos(CueBallAngle)
                FirstXImpact = np.abs(FirstXImpact)
                NextCueBallLocationX_Y = CurrentCueBallLocationY + (PoolParams['TableLength'] - CurrentCueBallLocationX- PoolParams['BallDiameter']/2)*np.tan(CueBallAngle)
                NextCueBallLocationX_X = (PoolParams['TableLength'] - PoolParams['BallDiameter']/2)
                NextCueBallAngleX = np.angle(-(PoolParams['TableLength'] - CurrentCueBallLocationX- PoolParams['BallDiameter']/2) + 1j*(NextCueBallLocationX_Y - CurrentCueBallLocationY));
          
            elif np.cos(CueBallAngle) < 0 :
                FirstXImpact = (CurrentCueBallLocationX- PoolParams['BallDiameter']/2)/np.cos(CueBallAngle)
                FirstXImpact = np.abs(FirstXImpact)
                NextCueBallLocationX_Y = CurrentCueBallLocationY - (CurrentCueBallLocationX- PoolParams['BallDiameter']/2)*np.tan(CueBallAngle)
                NextCueBallLocationX_X = (PoolParams['BallDiameter']/2)
                NextCueBallAngleX = np.angle((CurrentCueBallLocationX- PoolParams['BallDiameter']/2) - 1j*(NextCueBallLocationX_Y - CurrentCueBallLocationY));
            else:
                FirstXImpact = 9999
            
            if FirstXImpact < FirstYImpact:
                NextImpactDistance = FirstXImpact
                NextCueBallLocationY = NextCueBallLocationX_Y
                NextCueBallLocationX = NextCueBallLocationX_X
                NextCueBallAngle = NextCueBallAngleX
            else:
                NextImpactDistance = FirstYImpact
                NextCueBallLocationY = NextCueBallLocationY_Y
                NextCueBallLocationX = NextCueBallLocationY_X
                NextCueBallAngle = NextCueBallAngleY
            
            TravelDistance = np.sqrt(((NextCueBallLocationX-CurrentCueBallLocationX)**2) + ((NextCueBallLocationY-CurrentCueBallLocationY)**2))
            
            ImpactWithBall = 0
            ImpactWithPocket = 0
            
            CueBallDistToObjectBall = np.zeros(len(UnpottedBalls))
            CueBallAngleToObjectBall = np.zeros(len(UnpottedBalls))
            CueToObjectAngleThreshold = np.zeros(len(UnpottedBalls))
    
            NoCushions[0,I-1] = J
            
            for K in range(1,len(UnpottedBalls)):
                CueBallDistToObjectBallX = BallLocationX[UnpottedBalls[K]] - CurrentCueBallLocationX;
                CueBallDistToObjectBallY = BallLocationY[UnpottedBalls[K]] - CurrentCueBallLocationY;
                CueBallDistToObjectBall[K] = np.sqrt((CueBallDistToObjectBallX**2) + (CueBallDistToObjectBallY**2))
                CueBallAngleToObjectBall[K] = np.angle(CueBallDistToObjectBallX + 1j*CueBallDistToObjectBallY);
                CueToObjectAngleThreshold[K] = np.abs(np.arcsin(PoolParams['BallDiameter']/CueBallDistToObjectBall[K]));
            
            OrderedCueBallDistToObjectBall = np.argsort(CueBallDistToObjectBall)
                
            for K in range(1,len(OrderedCueBallDistToObjectBall)):    
                if CueBallDistToObjectBall[OrderedCueBallDistToObjectBall[K]] < NextImpactDistance:
                    if (CueBallAngle > (CueBallAngleToObjectBall[OrderedCueBallDistToObjectBall[K]] - CueToObjectAngleThreshold[OrderedCueBallDistToObjectBall[K]])) & (CueBallAngle < (CueBallAngleToObjectBall[OrderedCueBallDistToObjectBall[K]] + CueToObjectAngleThreshold[OrderedCueBallDistToObjectBall[K]])):
                        ImpactWithBall = 1
                        if (ColorAssignment[Player-1] == 0) | ((ColorAssignment[Player-1] == 1)
                            & (UnpottedBalls[OrderedCueBallDistToObjectBall[K]] < (9-CannotStrikeBlack))) | ((ColorAssignment[Player-1] == 2) 
                            & (UnpottedBalls[OrderedCueBallDistToObjectBall[K]] > (7+CannotStrikeBlack))):   
                            TotalTravelDistance[0,I-1] = TotalTravelDistance[0,I-1] + CueBallDistToObjectBall[OrderedCueBallDistToObjectBall[K]]
                            BallStruck[0,I-1] = UnpottedBalls[OrderedCueBallDistToObjectBall[K]]
                            NoCushions[0,I-1] = J
                            break
                            
                        else:
                            TotalTravelDistance[0,I-1] = 9999
                            BallStruck[0,I-1] = UnpottedBalls[OrderedCueBallDistToObjectBall[K]]
                            NoCushions[0,I-1] = J
                            break
            
            for K in range(0,len(PocketLocations)):  
                if np.abs(PocketLocations[K,0] -  NextCueBallLocationX) < PoolParams['BallDiameter']:
                    if np.abs(PocketLocations[K,1] -  NextCueBallLocationY)< PoolParams['BallDiameter']:
                        ImpactWithPocket = 1;
                        TotalTravelDistance[0,I-1] = 9999
                        BallStruck[0,I-1] = 7777
                        NoCushions[0,I-1] = J
                        break
                
                
                        
            
            if ImpactWithBall == 1 or ImpactWithPocket == 1:
                break
            else:
               TotalTravelDistance[0,I-1] = TotalTravelDistance[0,I-1] + TravelDistance
               CueBallAngle = NextCueBallAngle
               CurrentCueBallLocationX = NextCueBallLocationX
               CurrentCueBallLocationY = NextCueBallLocationY
        
       
    OptimalStrokeAngle = 2*np.pi *(np.argmin(TotalTravelDistance)+1)/NoAnglesToTry - np.pi
    return(OptimalStrokeAngle)

        