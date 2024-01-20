import {
  SciChartSurface,
  NumericAxis,
  FastLineRenderableSeries,
  XyDataSeries,
  EllipsePointMarker,
  SweepAnimation,
  SciChartJsNavyTheme,
  NumberRange
} from "scichart";

async function FichesChart() {
  // Insérez ici la clé de licence si nécessaire
  // SciChartSurface.setRuntimeLicenseKey("YOUR_RUNTIME_KEY");

  const { sciChartSurface, wasmContext } = await SciChartSurface.create("chart-container", {
    theme: new SciChartJsNavyTheme(),
    title: "Fiches fabrication",
    titleStyle: { fontSize: 22 }
  });

  // Configurez les axes X et Y
  const growBy = new NumberRange(1, 1);
  sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "Axe X", growBy }));
  sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { axisTitle: "Axe Y", growBy }));

  sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, {
    stroke: "steelblue",
    strokeThickness: 3,
    dataSeries: new XyDataSeries(wasmContext, {
      xValues: [0,1,2,3,4,5,6,7,8,9],
      yValues: [0, 0.0998, 0.1986, 0.2955, 0.3894, 0.4794, 0.5646, 0.6442, 0.7173, 0.7833]
    }),
    pointMarker: new EllipsePointMarker(wasmContext, { width: 11, height: 11, fill: "#fff" }),
    animation: new SweepAnimation({ duration: 300, fadeEffect: true })
  }));

  return sciChartSurface;
}
