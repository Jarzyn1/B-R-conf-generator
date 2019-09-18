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
<LN ID="%IW.#module_path#.AnalogInput01" Type="INT">
<Prod Device="#module_path#" DPName="AnalogInput01" Kind="io"/>
#ai01#
</LN>
<LN ID="%IW.#module_path#.AnalogInput02" Type="INT">
<Prod Device="#module_path#" DPName="AnalogInput02" Kind="io"/>
#ai02#
</LN>
<LN ID="%IB.#module_path#.StatusInput01" Type="USINT">
<Prod Device="#module_path#" DPName="StatusInput01" Kind="io"/>
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
