<template>
        <div class="card">
            <div class="card-body">

    <div style="width: 100%; display: flex; justify-content: space-between">
      <!-- <div id="myPaletteDiv" style="width: 100px; margin-right: 2px; background-color: whitesmoke; border: solid 1px black"></div> -->
      <div id="myDiagramDiv" style="flex-grow: 1; height: 1500px;"></div>
    </div>
</div>
  </div>
</template>



<script>
export default {
  name: 'script',
  data(){
    return {
      myDiagram:{},
      mySavedModel:{ "copiesArrays": true, "copiesArrayObjects": true, "nodeDataArray": [ { "key": 1, "text": "nginx-front-xiaoniu" }, { "key": 2, "text": "nginx-front-be"}, { "key": 3, "text": "nginx-middle-mobile" }, { "key": 4, "text": "nginx-middle-pic" }, { "key": 5, "text": "nginx-middle-xiaoniu" }, { "key": 6, "text": "web-8000-be" }, { "key": 7, "text": "web-8100-crm" }, { "key": 8, "text": "web-8200-neo" }, { "key": 9, "text": "web-7038-fund" }, { "key": 10, "text": "tomcat-7038-fund" }, { "key": 11, "text": "tomcat-9001-user" }, { "key": 12, "text": "tomcat-9003-product" }, { "key": 13, "text": "tomcat-9007-weixin" }, { "key": 14, "text": "tomcat-9008-portal" }, { "key": 15, "text": "tomcat-9010-payment" }, { "key": 16, "text": "tomcat-9012-cms", "category": "Success" }, { "key": 17, "text": "tomcat-9018-partner", "category": "Warning","ips":["1.1.1.1","2.2.2.2"] }, { "key": 18, "text": "redis-session","category":"Error" }, { "key": 19, "text": "mongedb" }, { "key": 20, "text": "mysql" }, { "key": 21, "text": "ZK" } ], "linkDataArray": [ { "from": 1, "to": 8 }, { "from": 2, "to": 6 }, { "from": 3, "to": 10 }, { "from": 3, "to": 11 }, { "from": 3, "to": 12 }, { "from": 3, "to": 13 }, { "from": 3, "to": 14 }, { "from": 3, "to": 15 }, { "from": 3, "to": 16 }, { "from": 3, "to": 17 }, { "from": 10, "to": 18}, { "from": 11, "to": 18}, { "from": 12, "to": 18}, { "from": 13, "to": 18}, { "from": 14, "to": 18}, { "from": 15, "to": 18}, { "from": 16, "to": 18}, { "from": 17, "to": 18}, { "from": 10, "to": 20}, { "from": 11, "to": 20}, { "from": 12, "to": 20}, { "from": 13, "to": 20}, { "from": 14, "to": 20}, { "from": 15, "to": 20}, { "from": 16, "to": 20}, { "from": 16, "to": 17}, { "from": 11, "to": 21}, { "from": 13, "to": 19}, { "from": 17, "to": 20} ] }

    }
  },
  methods: {
    init() {
      // if (window.goSamples) goSamples(); // init for these samples -- you don't need to call this
      var $ = go.GraphObject.make; // for conciseness in defining templates
      var yellowgrad = $(go.Brush, "Linear", { 0: "rgb(254, 201, 0)", 1: "rgb(254, 162, 0)" });
      var greengrad = $(go.Brush, "Linear", { 0: "#98FB98", 1: "#9ACD32" });
      var bluegrad = $(go.Brush, "Linear", { 0: "#B0E0E6", 1: "#87CEEB" });
      var redgrad = $(go.Brush, "Linear", { 0: "#C45245", 1: "#871E1B" });
      var whitegrad = $(go.Brush, "Linear", { 0: "#F0F8FF", 1: "#E6E6FA" });
      var bigfont = "bold 13pt Helvetica, Arial, sans-serif";
      var smallfont = "bold 11pt Helvetica, Arial, sans-serif";
      // Common text styling
      function textStyle() {
        return {
          margin: 6,
          wrap: go.TextBlock.WrapFit,
          textAlign: "center",
          editable: false,
          font: bigfont
        }
      }
      console.log('a---------------',go)
      var myDiagram = $(go.Diagram, "myDiagramDiv", {
          // have mouse wheel events zoom in and out instead of scroll up and down
          // "toolManager.mouseWheelBehavior": go.ToolManager.WheelZoom,
          allowDrop: true, // support drag-and-drop from the Palette
          initialAutoScale: go.Diagram.Uniform,
          // "linkingTool.direction": go.LinkingTool.ForwardsOnly,
          // initialContentAlignment: go.Spot.Center,
          layout: $(go.LayeredDigraphLayout, { isInitial: false, isOngoing: false, layerSpacing: 50 }),
          "undoManager.isEnabled": true
        });
      console.log('bbbbbbbbbbbbbbbb---------------')
      // define the Node template
      function nodeInfo(d) { // Tooltip info for a node data object
        var str = d.text + "\n";
        console.log(d, 'd............')
        if (d.ips) {
          str += "ip:\n";
          for (var n in d.ips) {
            str += '' + d.ips[n] + '\n';
          }
        }
        return str;
      }
      var tooltiptemplate =
        $(go.Adornment, "Auto",
          $(go.Shape, "Rectangle", { fill: "whitesmoke", stroke: "black" }),
          $(go.TextBlock, {
              font: "bold 8pt Helvetica, bold Arial, sans-serif",
              wrap: go.TextBlock.WrapFit,
              margin: 5
            },
            new go.Binding("text", "", nodeInfo))
        );

      console.log('b---------------------------')
      myDiagram.nodeTemplate =
        $(go.Node, "Auto",
          // { selectionAdornmentTemplate: defaultAdornment },
          { toolTip: tooltiptemplate },
          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          // define the node's outer shape, which will surround the TextBlock
          $(go.Shape, "Rectangle", {
            fill: whitegrad,
            stroke: "black",
            portId: "",
            fromLinkable: true,
            toLinkable: true,
            cursor: "pointer",
            toEndSegmentLength: 50,
            fromEndSegmentLength: 40
          }),
          $(go.TextBlock, "Page", {
              margin: 6,
              font: bigfont,
              editable: false
            },
            new go.Binding("text", "text").makeTwoWay()),
        );



      myDiagram.nodeTemplateMap.add("Success",
        $(go.Node, "Auto", { toolTip: tooltiptemplate },

          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, "RoundedRectangle", {
            fill: greengrad,
            portId: "",
            fromLinkable: true,
            cursor: "pointer",
            fromEndSegmentLength: 40
          }),
          $(go.TextBlock, "Success", textStyle(),
            new go.Binding("text", "text").makeTwoWay())
        ),
      );
      myDiagram.nodeTemplateMap.add("Warning",
        $(go.Node, "Auto", { toolTip: tooltiptemplate },
          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, "RoundedRectangle", { fill: yellowgrad, portId: "", toLinkable: true, toEndSegmentLength: 50 }),
          $(go.TextBlock, "Warning", textStyle(),
            new go.Binding("text", "text").makeTwoWay())
        ),

      );
      myDiagram.nodeTemplateMap.add("Error",
        $(go.Node, "Auto", { toolTip: tooltiptemplate },

          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, "RoundedRectangle", { fill: redgrad, portId: "", toLinkable: true, toEndSegmentLength: 50 }),
          $(go.TextBlock, "Error", textStyle(),
            new go.Binding("text", "text").makeTwoWay())
        ),
      );

      myDiagram.linkTemplate =
        $(go.Link, // the whole link panel
          new go.Binding("points").makeTwoWay(), { curve: go.Link.Bezier, toShortLength: 15 },
          new go.Binding("curviness", "curviness"),
          $(go.Shape, // the link shape
            { stroke: "#2F4F4F", strokeWidth: 2.5 }),
          $(go.Shape, // the arrowhead
            { toArrow: "kite", fill: "#2F4F4F", stroke: null, scale: 2 })
        );
      myDiagram.linkTemplateMap.add("Comment",
        $(go.Link, { selectable: false },
          $(go.Shape, { strokeWidth: 2, stroke: "darkgreen" })));

      // read in the JSON-format data from the "mySavedModel" element

      this.myDiagram = myDiagram
      this.load();
      this.layout();
    },
     layout() {
      this.myDiagram.layoutDiagram(true);
    },
     load() {
      // this.myDiagram.model = go.Model.fromJson(document.getElementById("mySavedModel").value);
      console.log('ccccccccccc',this.mySavedModel)
      this.myDiagram.model = go.Model.fromJson(this.mySavedModel)
    },

  },
  mounted() {
    this.init()
  }
}

</script>
