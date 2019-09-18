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
<LN ID="%ID.#module_path#.EthRxLost" Type="DINT">
<Prod Device="#module_path#" DPName="EthRxLost" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthRxOversize" Type="DINT">
<Prod Device="#module_path#" DPName="EthRxOversize" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthRxCRCError" Type="DINT">
<Prod Device="#module_path#" DPName="EthRxCRCError" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthRxOverflow" Type="DINT">
<Prod Device="#module_path#" DPName="EthRxOverflow" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthTxCollision" Type="DINT">
<Prod Device="#module_path#" DPName="EthTxCollision" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.EthPhy1LinkOk" Type="BOOL">
<Prod Device="#module_path#" DPName="EthPhy1LinkOk" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthPhy1LinkLoss" Type="DINT">
<Prod Device="#module_path#" DPName="EthPhy1LinkLoss" Kind="io"/>
</LN>
<LN ID="%IX.#module_path#.EthPhy2LinkOk" Type="BOOL">
<Prod Device="#module_path#" DPName="EthPhy2LinkOk" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.EthPhy2LinkLoss" Type="DINT">
<Prod Device="#module_path#" DPName="EthPhy2LinkLoss" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.Nettime" Type="DINT">
<Prod Device="#module_path#" DPName="Nettime" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.CycleCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.CycleCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.BreakCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.BreakCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncBusyErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncBusyErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncNoRxErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncNoRxErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncFormatErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncFormatErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncPendingErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncPendingErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncBusyErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncBusyErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncNoRxErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncNoRxErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncFormatErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncFormatErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncPendingErrorCount" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncPendingErrorCount" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.ModuleLostWhileOperational" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.ModuleLostWhileOperational" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.ModuleNewWhileOperational" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.ModuleNewWhileOperational" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.IF1.StationAtBusEnd" Type="USINT">
<Prod Device="#module_path#" DPName="IF1.StationAtBusEnd" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.StationAtBusEndChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="IF1.StationAtBusEndChangeTime" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.IF1.StationPastOutFrameError" Type="USINT">
<Prod Device="#module_path#" DPName="IF1.StationPastOutFrameError" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.StationPastOutFrameErrorChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="IF1.StationPastOutFrameErrorChangeTime" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.IF1.StationPastInFrameError" Type="USINT">
<Prod Device="#module_path#" DPName="IF1.StationPastInFrameError" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.StationPastInFrameErrorChangeTime" Type="DATE_AND_TIME">
<Prod Device="#module_path#" DPName="IF1.StationPastInFrameErrorChangeTime" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.IF1.NrOfStationsMax" Type="USINT">
<Prod Device="#module_path#" DPName="IF1.NrOfStationsMax" Kind="io"/>
</LN>
<LN ID="%IB.#module_path#.IF1.NrOfStationsConfigured" Type="USINT">
<Prod Device="#module_path#" DPName="IF1.NrOfStationsConfigured" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncInFrameSize" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncInFrameSize" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.SyncOutFrameSize" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.SyncOutFrameSize" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncFrameSize" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncFrameSize" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.AsyncFrameSpareSize" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.AsyncFrameSpareSize" Kind="io"/>
</LN>
<LN ID="%ID.#module_path#.IF1.BusLengthConfigured" Type="DINT">
<Prod Device="#module_path#" DPName="IF1.BusLengthConfigured" Kind="io"/>
</LN>

</Links>
</IO>
