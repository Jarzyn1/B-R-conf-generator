<?xmlversion="1.0" encoding="utf-8"?>
<?AutomationRuntimeIOSystem Version="1.0"?>
<IO xmlns="http://www.br-automation.com/AR/IO">
<Links>
<LN ID="%IX.#module_path#.ModuleOk" Type="BOOL">
<Prod Device="#module_path#" DPName="ModuleOk" Kind="io"/>
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
<LN ID="%QX.#module_path#.DigitalOutput02" Type="BOOL">
#do02#
<Cons Device="#module_path#" DPName="DigitalOutput02" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput03" Type="BOOL">
#do03#
<Cons Device="#module_path#" DPName="DigitalOutput03" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput04" Type="BOOL">
#do04#
<Cons Device="#module_path#" DPName="DigitalOutput04" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput05" Type="BOOL">
#do05#
<Cons Device="#module_path#" DPName="DigitalOutput05" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput06" Type="BOOL">
#do06#
<Cons Device="#module_path#" DPName="DigitalOutput06" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput07" Type="BOOL">
#do07#
<Cons Device="#module_path#" DPName="DigitalOutput07" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput08" Type="BOOL">
#do08#
<Cons Device="#module_path#" DPName="DigitalOutput08" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput09" Type="BOOL">
#do09#
<Cons Device="#module_path#" DPName="DigitalOutput09" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput10" Type="BOOL">
#do10#
<Cons Device="#module_path#" DPName="DigitalOutput10" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput11" Type="BOOL">
#do11#
<Cons Device="#module_path#" DPName="DigitalOutput11" Kind="io"/>
</LN>
<LN ID="%QX.#module_path#.DigitalOutput12" Type="BOOL">
#do12#
<Cons Device="#module_path#" DPName="DigitalOutput12" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput01" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput01" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput02" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput02" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput03" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput03" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput04" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput04" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput05" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput05" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput06" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput06" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput07" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput07" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput08" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput08" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput09" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput09" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput10" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput10" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput11" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput11" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.StatusDigitalOutput12" Type="BOOL">
<Prod Device="#module_path#" DPName="StatusDigitalOutput12" Kind="io"/>
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
