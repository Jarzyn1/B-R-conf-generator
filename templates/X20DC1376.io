<?xmlversion="1.0" encoding="utf-8"?>
<?AutomationRuntimeIOSystem Version="1.0"?>
<IO xmlns="http://www.br-automation.com/AR/IO">
<Links>
<LN ID="%IX.#module_path#.ModuleOk" Type="BOOL">
<Prod Device="#module_path#" DPName="ModuleOk" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StaleData" Type="BOOL">
<Prod Device="#module_path#" DPName="StaleData" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.SerialNumber" Type="UDINT">
<Prod Device="#module_path#" DPName="SerialNumber" Kind="io"/>
</LN>
<LN ID="%IW.#module_path#.ModuleID" Type="UINT">
<Prod Device="#module_path#" DPName="ModuleID" Kind="io"/>
</LN>
<LN ID="%IW.#module_path#.HardwareVariant" Type="UINT">
<Prod Device="#module_path#" DPName="HardwareVariant" Kind="io"/>
</LN>
<LN ID="%IW.#module_path#.FirmwareVersion" Type="UINT">
<Prod Device="#module_path#" DPName="FirmwareVersion" Kind="io"/>
</LN>
<LN ID="%IW.#module_path#.Encoder01" Type="INT">
<Prod Device="#module_path#" DPName="Encoder01" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.Encoder01Reset" Type="BOOL">
<Cons Device="#module_path#" DPName="Encoder01Reset" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.DigitalInput01" Type="BOOL">
<Prod Device="#module_path#" DPName="DigitalInput01" Kind="io"/>
#di01#
</LN>
<LN ID="%IX.#module_path#.DigitalInput02" Type="BOOL">
<Prod Device="#module_path#" DPName="DigitalInput02" Kind="io"/>
#di02#
</LN>
<LN ID="%IX.#module_path#.BW_Channel_A" Type="BOOL">
<Prod Device="#module_path#" DPName="BW_Channel_A" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.BW_QuitChannel_A" Type="BOOL">
<Cons Device="#module_path#" DPName="BW_QuitChannel_A" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.BW_Channel_B" Type="BOOL">
<Prod Device="#module_path#" DPName="BW_Channel_B" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.BW_QuitChannel_B" Type="BOOL">
<Cons Device="#module_path#" DPName="BW_QuitChannel_B" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.BW_Channel_R" Type="BOOL">
<Prod Device="#module_path#" DPName="BW_Channel_R" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.BW_QuitChannel_R" Type="BOOL">
<Cons Device="#module_path#" DPName="BW_QuitChannel_R" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.PowerSupply01" Type="BOOL">
<Prod Device="#module_path#" DPName="PowerSupply01" Kind="io"/>
</LN>
<LN ID="%IW.#module_path#.BusModuleId" Type="UINT">
<Prod Device="#module_path#" DPName="BusModuleId" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.ModeOfOperation" Type="USINT">
<Prod Device="#module_path#" DPName="ModeOfOperation" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.ModeOfOperationChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="ModeOfOperationChangeTime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfResets" Type="DINT">
<Prod Device="#module_path#" DPName="NrOfResets" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfResetsChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="NrOfResetsChangeTime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfInits" Type="DINT">
<Prod Device="#module_path#" DPName="NrOfInits" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfInitsChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="NrOfInitsChangeTime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfFwUpdates" Type="DINT">
<Prod Device="#module_path#" DPName="NrOfFwUpdates" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.NrOfFwUpdatesChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="NrOfFwUpdatesChangeTime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.ModuleNoComm" Type="DINT">
<Prod Device="#module_path#" DPName="ModuleNoComm" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.ModuleNoCommChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="ModuleNoCommChangeTime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.ModuleCommError" Type="DINT">
<Prod Device="#module_path#" DPName="ModuleCommError" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.ModuleCommErrorChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="ModuleCommErrorChangeTime" Kind="io"/>
</LN>

</Links>
</IO>
