from DobotRPC import DobotlinkAdapter, RPCClient


class DType(object):
    def __init__(self):
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    # def search_dobot(self):
    #     return self.__dobotlink.M1.SearchDobot()

    # def connect_dobot(self, api, queue_start=True):
    #     return self.__dobotlink.M1.ConnectDobot(portName=api,
    #                                             queueStart=queue_start)

    # def disconnect_dobot(self, api, queue_stop=True, queue_clear=True):
    #     return self.__dobotlink.M1.DisconnectDobot(portName=api,
    #                                                queueStop=queue_stop,
    #                                                queueClear=queue_clear)

    # def get_devicesn(self, api):
    #     return self.__dobotlink.M1.GetDeviceSN(portName=api)

    # def set_devicename(self, api, device_name):
    #     return self.__dobotlink.M1.SetDeviceName(portName=api,
    #                                              deviceName=device_name)

    # def get_devicename(self, api):
    #     return self.__dobotlink.M1.GetDeviceName(portName=api)

    # def get_deviceversion(self, api, get_type: int):
    #     return self.__dobotlink.M1.GetDeviceVersion(portName=api,
    #                                                 type=get_type)

    # def get_hardware_version(self, api):
    #     return self.__dobotlink.M1.GetHardwareVersion(portName=api)

    def QueuedCmdStart(self, api):
        return self.__dobotlink.M1.QueuedCmdStart(portName=api)

    def QueuedcmdStop(self, api, force_stop=False):
        return self.__dobotlink.M1.QueuedCmdStop(portName=api,
                                                 forceStop=force_stop)

    # def queuedcmd_clear(self, api):
    #     return self.__dobotlink.M1.QueuedCmdClear(portName=api)

    # def queuedcmd_startdownload(self, api, total_loop, lineper_loop):
    #     return self.__dobotlink.M1.QueuedCmdStartDownload(
    #         portName=api, totalLoop=total_loop, linePerLoop=lineper_loop)

    # def queuedcmd_stopdownload(self, api):
    #     return self.__dobotlink.M1.QueuedCmdStopDownload(portName=api)

    # def get_queuedcmd_currentindex(self, api):
    #     return self.__dobotlink.M1.GetQueuedCmdCurrentIndex(portName=api)

    # def get_queuedcmd_leftspace(self, api):
    #     return self.__dobotlink.M1.GetQueuedCmdLeftSpace(portName=api)

    def GetPose(self, api):
        result = self.__dobotlink.M1.GetPose(portName=api)
        return [
            result["x"], result["y"], result["z"], result["r"],
            result["jointAngle"][0], result["jointAngle"][1],
            result["jointAngle"][2], result["jointAngle"][3]
        ]

    # def reset_pose(self, api, front_angle1, front_angle2):
    #     return self.__dobotlink.M1.ResetPose(portName=api,
    #                                          frontAngle1=front_angle1,
    #                                          frontAngle2=front_angle2)

    def SetUserCoordinate(self, api, x: float, y: float, z: float, r: float):
        self.__dobotlink.M1.SetUserCoordinate(portName=api,
                                              x=x,
                                              y=y,
                                              z=z,
                                              r=r,
                                              isQueued=True)

    def GetUserCoordinate(self, api):
        result = self.__dobotlink.M1.GetUserCoordinate(portName=api)
        return [result["x"], result["y"], result["z"], result["r"]]

    def SetToolCoordinate(self, api, x: float, y: float, z: float, r: float):
        self.__dobotlink.M1.SetToolCoordinate(portName=api,
                                              x=x,
                                              y=y,
                                              z=z,
                                              r=r,
                                              isQueued=True)

    def GetToolCoordinate(self, api):
        result = self.__dobotlink.M1.GetToolCoordinate(portName=api)
        return [result["x"], result["y"], result["z"], result["r"]]

    # def get_alarms_state(self, api):
    #     return self.__dobotlink.M1.GetAlarmsState(portName=api)

    # def clear_allalarms_state(self, api):
    #     return self.__dobotlink.M1.ClearAllAlarmsState(portName=api)

    # def get_run_state(self, api):
    #     return self.__dobotlink.M1.GetRunState(portName=api)

    # def set_homecmd(self,
    #                 api,
    #                 is_resetpars=False,
    #                 is_queued=True,
    #                 iswait_forfinish=True,
    #                 time_out=25000):
    #     return self.__dobotlink.M1.SetHOMECmd(portName=api,
    #                                           isResetPars=is_resetpars,
    #                                           isQueued=is_queued,
    #                                           isWaitForFinish=iswait_forfinish,
    #                                           timeout=time_out)

    # def set_home_initialpos(self, api):
    #     return self.__dobotlink.M1.SetHOMEInitialPos(portName=api)

    # def set_hhttrig_mode(self, api, mode: int, is_queued=False):
    #     return self.__dobotlink.M1.SetHHTTrigMode(portName=api,
    #                                               mode=mode,
    #                                               isQueued=is_queued)

    # def get_hhttrig_mode(self, api):
    #     return self.__dobotlink.M1.GetHHTTrigMode(portName=api)

    # def set_hhttrig_output_enabled(self, api, enable: bool, is_queued=False):
    #     return self.__dobotlink.M1.SetHHTTrigOutputEnabled(portName=api,
    #                                                        enable=enable,
    #                                                        isQueued=is_queued)

    # def get_hhttrig_output_enabled(self, api):
    #     return self.__dobotlink.M1.GetHHTTrigOutputEnabled(portName=api)

    # def get_hhttrig_output(self, api):
    #     return self.__dobotlink.M1.GetHHTTrigOutput(portName=api)

    # def set_servo_power(self, api, on: bool, is_queued=False):
    #     return self.__dobotlink.M1.SetServoPower(portName=api,
    #                                              on=on,
    #                                              isQueued=is_queued)

    # def set_endeffector_params(self,
    #                            api,
    #                            x_offset: float,
    #                            y_offset: float,
    #                            z_offset: float,
    #                            is_queued=False):
    #     return self.__dobotlink.M1.SetEndEffectorParams(portName=api,
    #                                                     xOffset=x_offset,
    #                                                     yOffset=y_offset,
    #                                                     zOffset=z_offset,
    #                                                     isQueued=is_queued)

    # def get_endeffector_params(self, api):
    #     return self.__dobotlink.M1.GetEndEffectorParams(portName=api)

    # def set_endeffector_laser(self,
    #                           api,
    #                           enable: bool,
    #                           on: bool,
    #                           is_queued=False):
    #     return self.__dobotlink.M1.SetEndEffectorLaser(portName=api,
    #                                                    enable=enable,
    #                                                    on=on,
    #                                                    isQueued=is_queued)

    # def get_endeffector_laser(self, api):
    #     return self.__dobotlink.M1.GetEndEffectorLaser(portName=api)

    # def set_endeffector_suctioncup(self,
    #                                api,
    #                                enable: bool,
    #                                on: bool,
    #                                is_queued=False):
    #     return self.__dobotlink.M1.SetEndEffectorSuctionCup(portName=api,
    #                                                         enable=enable,
    #                                                         on=on,
    #                                                         isQueued=is_queued)

    # def get_endeffector_suctioncup(self, api):
    #     return self.__dobotlink.M1.GetEndEffectorSuctionCup(portName=api)

    # def set_endeffector_gripper(self,
    #                             api,
    #                             enable: bool,
    #                             on: bool,
    #                             is_queued=False):
    #     return self.__dobotlink.M1.SetEndEffectorGripper(portName=api,
    #                                                      enable=enable,
    #                                                      on=on,
    #                                                      isQueued=is_queued)

    # def get_endeffector_gripper(self, api):
    #     return self.__dobotlink.M1.GetEndEffectorGripper(portName=api)

    # def set_jogjoint_params(self,
    #                         api,
    #                         velocity,
    #                         acceleration,
    #                         is_queued=False):
    #     return self.__dobotlink.M1.SetJOGJointParams(portName=api,
    #                                                  velocity=velocity,
    #                                                  acceleration=acceleration,
    #                                                  isQueued=is_queued)

    # def get_jogjoint_params(self, api):
    #     return self.__dobotlink.M1.GetJOGJointParams(portName=api)

    # def set_jogcoordinate_params(self,
    #                              api,
    #                              velocity,
    #                              acceleration,
    #                              is_queued=False):
    #     return self.__dobotlink.M1.SetJOGCoordinateParams(
    #         portName=api,
    #         velocity=velocity,
    #         acceleration=acceleration,
    #         isQueued=is_queued)

    # def get_jogcoordinate_params(self, api):
    #     return self.__dobotlink.M1.GetJOGCoordinateParams(portName=api)

    # def set_jogcommon_params(self,
    #                          api,
    #                          velocity_ratio,
    #                          acceleration_ratio,
    #                          is_queued=False):
    #     return self.__dobotlink.M1.SetJOGCommonParams(
    #         portName=api,
    #         velocityRatio=velocity_ratio,
    #         accelerationRatio=acceleration_ratio,
    #         isQueued=is_queued)

    # def get_jogcommon_params(self, api):
    #     return self.__dobotlink.M1.GetJOGCommonParams(portName=api)

    # def set_jogcmd(self, api, is_joint, cmd, is_queued):
    #     return self.__dobotlink.M1.SetJOGCmd(portName=api,
    #                                          isJoint=is_joint,
    #                                          cmd=cmd,
    #                                          isQueued=is_queued)

    # def set_inchmode(self, api, mode: int):
    #     return self.__dobotlink.M1.SetInchMode(portName=api, mode=mode)

    # def get_inchmode(self, api):
    #     return self.__dobotlink.M1.GetInchMode(portName=api)

    # def set_inchparam(self, api, distance_mm: float, distance_ang: float):
    #     return self.__dobotlink.M1.SetInchParam(portName=api,
    #                                             distanceMM=distance_mm,
    #                                             distanceANG=distance_ang)

    # def get_inchparam(self, api):
    #     return self.__dobotlink.M1.GetInchParam(portName=api)

    def SetPTPCmdSync(self, api, ptpMode, x, y, z, rHead):
        self.__dobotlink.M1.SetPTPCmd(portName=api,
                                      ptpMode=ptpMode,
                                      x=x,
                                      y=y,
                                      z=z,
                                      r=rHead,
                                      timeout=2000000000,
                                      isQueued=True,
                                      isWaitForFinish=True)

    def SetPTPPOCmdSync(self, api, ptpMode, x, y, z, rHead, poCmd):
        po_cmd = []
        for po in poCmd:
            po_cmd.append({"ratio": po[0], "port": po[1], "level": po[2]})
        self.__dobotlink.M1.SetPTPPOCmd(portName=api,
                                        ptpCmd={
                                            "ptpMode": ptpMode,
                                            "x": x,
                                            "y": y,
                                            "z": z,
                                            "r": rHead
                                        },
                                        poCmd=po_cmd,
                                        isQueued=True,
                                        isWaitForFinish=True)

    # def set_ptpjoint_param(self, api, velocity, acceleration,
    # is_queued=False):
    #     return self.__dobotlink.M1.SetPTPJointParams(portName=api,
    #                                                  velocity=velocity,
    #                                                  acceleration=acceleration,
    #                                                  isQueued=is_queued)

    # def get_ptpjoint_param(self, api):
    #     return self.__dobotlink.M1.GetPTPJointParams(portName=api)

    # def set_ptpcoordinate_params(self,
    #                              api,
    #                              xyz_velocity,
    #                              r_velocity,
    #                              xyz_acceleration,
    #                              r_acceleration,
    #                              is_queued=False):
    #     return self.__dobotlink.M1.SetPTPCoordinateParams(
    #         portName=api,
    #         xyzVelocity=xyz_velocity,
    #         rVelocity=r_velocity,
    #         xyzAcceleration=xyz_acceleration,
    #         rAcceleration=r_acceleration,
    #         isQueued=is_queued)

    # def get_ptpcoordinate_params(self, api):
    #     return self.__dobotlink.M1.GetPTPCoordinateParams(portName=api)

    def SetPTPJumpParams(self, api, jumpHeight, zLimit):
        self.__dobotlink.M1.SetPTPJumpParams(portName=api,
                                             zLimit=zLimit,
                                             jumpHeight=jumpHeight,
                                             isQueued=True)

    def GetPTPJumpParams(self, api):
        result = self.__dobotlink.M1.GetPTPJumpParams(portName=api)
        return [result["jumpHeight"], result["zLimit"]]

    def SetPTPCommonParams(self, api, velocityRatio, accelerationRatio):
        self.__dobotlink.M1.SetPTPCommonParams(
            portName=api,
            velocityRatio=velocityRatio,
            accelerationRatio=accelerationRatio,
            isQueued=True)

    def GetPTPCommonParams(self, api):
        result = self.__dobotlink.M1.GetPTPCommonParams(portName=api)
        return [result["velocityRatio"], result["accelerationRatio"]]

    # def set_motivation_mode(self, api, mode: int):
    #     return self.__dobotlink.M1.SetMotivationMode(portName=api, mode=mode)

    # def get_motivation_mode(self, api):
    #     return self.__dobotlink.M1.GetMotivationMode(portName=api)

    # def set_motivate_cmd(self,
    #                      api,
    #                      q1,
    #                      q2,
    #                      dq1,
    #                      dq2,
    #                      ddq1,
    #                      ddq2,
    #                      is_queued: bool,
    #                      iswait_forfinish,
    #                      time_out=10000):
    #     return self.__dobotlink.M1.SetMotivateCmd(
    #         portName=api,
    #         q1=q1,
    #         q2=q2,
    #         dq1=dq1,
    #         dq2=dq2,
    #         ddq1=ddq1,
    #         ddq2=ddq2,
    #         isQueued=is_queued,
    #         isWaitForFinish=iswait_forfinish,
    #         timeout=time_out)

    # def set_motivate_zcmd(self, api, qz, dqz, ddqz, is_queued: bool,
    #                       iswait_forfinish):
    #     return self.__dobotlink.M1.SetMotivateZCmd(
    #         portName=api,
    #         qz=qz,
    #         dqz=dqz,
    #         ddqz=ddqz,
    #         isQueued=is_queued,
    #         isWaitForFinish=iswait_forfinish)

    # def get_trajectory(self, api, count_max, index):
    #     return self.__dobotlink.M1.GetTrajectory(portName=api,
    #                                              countMax=count_max,
    #                                              index=index)

    def SetIODO(self, api, address, level):
        self.__dobotlink.M1.SetIODO(portName=api,
                                    port=address,
                                    level=level,
                                    isQueued=True)

    def GetIODO(self, api, addr):
        res = self.__dobotlink.M1.GetIODO(portName=api, port=addr)
        return [res["level"]]

    def GetIODI(self, api, addr):
        res = self.__dobotlink.M1.GetIODI(portName=api, port=addr)
        return [res["level"]]

    def GetIOADC(self, api, addr):
        res = self.__dobotlink.M1.GetIOADC(portName=api, port=addr)
        return [res["value"]]

    # def dSleep(self, s):
    #     time.sleep(s)

    # def set_cpparams(self,
    #                  api,
    #                  target_acc,
    #                  junction_vel,
    #                  isreal_timetrack,
    #                  acc=None,
    #                  period=None,
    #                  is_queued=False):
    #     return self.__dobotlink.M1.SetCPParams(
    #         portName=api,
    #         targetAcc=target_acc,
    #         junctionVel=junction_vel,
    #         isRealTimeTrack=isreal_timetrack,
    #         acc=acc,
    #         period=period,
    #         isQueued=is_queued)

    # def get_cpparams(self, api):
    #     return self.__dobotlink.M1.GetCPParams(portName=api)

    # def set_cpcmd(self, api, cp_mode, x, y, z, power, is_queued=False):
    #     return self.__dobotlink.M1.SetCPCmd(portName=api,
    #                                         cpMode=cp_mode,
    #                                         x=x,
    #                                         y=y,
    #                                         z=z,
    #                                         power=power,
    #                                         isQueued=is_queued)

    # def set_cplecmd(self, api, cp_mode, x, y, z, power, is_queued=False):
    #     return self.__dobotlink.M1.SetCPLECmd(portName=api,
    #                                           cpMode=cp_mode,
    #                                           x=x,
    #                                           y=y,
    #                                           z=z,
    #                                           power=power,
    #                                           isQueued=is_queued)

    # def set_arcparams(self,
    #                   api,
    #                   xyz_velocity,
    #                   r_velocity,
    #                   xyz_acceleration,
    #                   r_acceleration,
    #                   is_queued=False):
    #     return self.__dobotlink.M1.SetARCParams(
    #         portName=api,
    #         xyzVelocity=xyz_velocity,
    #         rVelocity=r_velocity,
    #         xyzAcceleration=xyz_acceleration,
    #         rAcceleration=r_acceleration,
    #         isQueued=is_queued)

    # def get_arcparams(self, api):
    #     return self.__dobotlink.M1.GetARCParams(portName=api)

    def SetARCCmdSync(self, api, cirPoint, toPoint):
        self.__dobotlink.M1.SetARCCmd(portName=api,
                                      cirPoint={
                                          "x": cirPoint[0],
                                          "y": cirPoint[1],
                                          "z": cirPoint[2],
                                          "r": cirPoint[3]
                                      },
                                      toPoint={
                                          "x": toPoint[0],
                                          "y": toPoint[1],
                                          "z": toPoint[2],
                                          "r": toPoint[3]
                                      },
                                      timeout=2000000000,
                                      isQueued=True,
                                      isWaitForFinish=True)

    # def set_arcpocmd(self, api, cir_point, to_point, arc_po, is_queued=False):
    #     return self.__dobotlink.M1.SetARCPOCmd(portName=api,
    #                                            cirPoint={
    #                                                "x": cirPoint[0],
    #                                                "y": cirPoint[1],
    #                                                "z": cirPoint[2],
    #                                                "r": cirPoint[3]
    #                                            },
    #                                            toPoint={
    #                                                "x": toPoint[0],
    #                                                "y": toPoint[1],
    #                                                "z": toPoint[2],
    #                                                "r": toPoint[3]
    #                                            },
    #                                            arcPO=arc_po,
    #                                            isQueued=is_queued)

    def SetCircleCmdSync(self, api, cirPoint, toPoint, count):
        self.__dobotlink.M1.SetCircleCmd(portName=api,
                                         cirPoint={
                                             "x": cirPoint[0],
                                             "y": cirPoint[1],
                                             "z": cirPoint[2],
                                             "r": cirPoint[3]
                                         },
                                         toPoint={
                                             "x": toPoint[0],
                                             "y": toPoint[1],
                                             "z": toPoint[2],
                                             "r": toPoint[3]
                                         },
                                         count=count,
                                         timeout=2000000000,
                                         isQueued=True,
                                         isWaitForFinish=True)

    # def set_circle_pocmd(self,
    #                      api,
    #                      cir_point,
    #                      to_point,
    #                      count,
    #                      circle_po,
    #                      is_queued=True):
    #     return self.__dobotlink.M1.SetCirclePOCmd(portName=api,
    #                                               cirPoint={
    #                                                   "x": cirPoint[0],
    #                                                   "y": cirPoint[1],
    #                                                   "z": cirPoint[2],
    #                                                   "r": cirPoint[3]
    #                                               },
    #                                               toPoint={
    #                                                   "x": toPoint[0],
    #                                                   "y": toPoint[1],
    #                                                   "z": toPoint[2],
    #                                                   "r": toPoint[3]
    #                                               },
    #                                               count=count,
    #                                               circlePO=circle_po,
    #                                               isQueued=is_queued)

    def SetArmOrientation(self, api, orientation):
        self.__dobotlink.M1.SetArmOrientation(portName=api,
                                              orientation=orientation,
                                              isQueued=True)

    def GetArmOrientation(self, api):
        result = self.__dobotlink.M1.GetArmOrientation(portName=api)
        return result["orientation"]

    def SetWAITCmdSync(self, api, delay):
        return self.__dobotlink.M1.SetWAITCmd(portName=api,
                                              delay=delay,
                                              timeout=delay + 500,
                                              isQueued=True,
                                              isWaitForFinish=True)

    # def set_safemode_enabled(self, api, enable):
    #     return self.__dobotlink.M1.SetSafeModeEnabled(portName=api,
    #                                                   enable=enable)

    # def get_safemode_enabled(self, api):
    #     return self.__dobotlink.M1.GetSafeModeEnabled(portName=api)

    # def set_collision_threshold(self, api, tor_diffj1, tor_diffj2, tor_diffj3,
    #                             tor_diffj4):
    #     return self.__dobotlink.M1.SetCollisionThreshold(portName=api,
    #                                                      torDiffJ1=tor_diffj1,
    #                                                      torDiffJ2=tor_diffj2,
    #                                                      torDiffJ3=tor_diffj3,
    #                                                      torDiffJ4=tor_diffj4)

    # def get_collision_threshold(self, api):
    #     return self.__dobotlink.M1.GetCollisionThreshold(portName=api)

    # def set_basicdynamic_params(self, api, zz1, fs1, fv1, zz2, mx2, my2, ia2,
    #                             fs2, fv2):
    #     return self.__dobotlink.M1.SetBasicDynamicParams(portName=api,
    #                                                      ZZ1=zz1,
    #                                                      FS1=fs1,
    #                                                      FV1=fv1,
    #                                                      ZZ2=zz2,
    #                                                      MX2=mx2,
    #                                                      MY2=my2,
    #                                                      IA2=ia2,
    #                                                      FS2=fs2,
    #                                                      FV2=fv2)

    # def get_basicdynamic_params(self, api):
    #     return self.__dobotlink.M1.GetBasicDynamicParams(portName=api)

    # def set_load_params(self, api, load_params):
    #     return self.__dobotlink.M1.SetLoadParams(portName=api,
    #                                              loadParams=load_params)

    # def get_load_params(self, api):
    #     return self.__dobotlink.M1.GetLoadParams(portName=api)

    # def set_safestrategy(self, api, strategy):
    #     return self.__dobotlink.M1.SetSafeStrategy(portName=api,
    #                                                strategy=strategy)

    # def get_safestrategy(self, api):
    #     return self.__dobotlink.M1.GetSafeStrategy(portName=api)

    # def set_safeguard_mode(self, api, mode):
    #     return self.__dobotlink.M1.SetSafeGuardMode(portName=api, mode=mode)

    # def get_safeguard_mode(self, api):
    #     return self.__dobotlink.M1.GetSafeGuardMode(portName=api)

    # def get_safeguard_status(self, api):
    #     return self.__dobotlink.M1.GetSafeGuardStatus(portName=api)

    # def set_lanport_config(self, api, addr, mask, gateway, dns, isdhcp):
    #     return self.__dobotlink.M1.SetLanPortConfig(portName=api,
    #                                                 addr=addr,
    #                                                 mask=mask,
    #                                                 gateway=gateway,
    #                                                 dns=dns,
    #                                                 isdhcp=isdhcp)

    # def get_lanport_config(self, api):
    #     return self.__dobotlink.M1.GetLanPortConfig(portName=api)

    # def set_firmware_reboot(self, api):
    #     return self.__dobotlink.M1.SetFirmwareReboot(portName=api)

    # def set_firmware_notifym4mode(self, api, mode):
    #     return self.__dobotlink.M1.SetFirmwareNotifyM4Mode(portName=api,
    #                                                        mode=mode)

    # def get_firmware_notifym4mode(self, api):
    #     return self.__dobotlink.M1.GetFirmwareNotifyM4Mode(portName=api)

    # def set_feed_forward(self, api, value):
    #     return self.__dobotlink.M1.SetFeedforward(portName=api, value=value)

    # def get_feed_forward(self, api):
    #     return self.__dobotlink.M1.GetFeedforward(portName=api)

    def SetTRIGCmdSync(self, api, address, mode, condition, threshold):
        self.__dobotlink.M1.SetTRIGCmd(portName=api,
                                       port=address,
                                       condition=condition,
                                       mode=mode,
                                       threshold=threshold,
                                       timeout=2000000000,
                                       isQueued=True,
                                       isWaitForFinish=True)
