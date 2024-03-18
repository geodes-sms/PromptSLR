import React from "react";

const getViewBox = (name: string) => {
  switch (name) {
    case "like":
      return "0 0 11 11";
    default:
      return "0 0 25 25";
  }
};

const getPath = (name: string, props: any) => {
  switch (name) {
    case "arrowDown":
      return (
        <>
          <defs>
            <style>
              {`.cls-2{fill:none;stroke:#333;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.5px}`}
            </style>
          </defs>
          <g id="Group_5123" transform="translate(.5 .5)">
            <g id="Group_4519" transform="translate(4.125 7.551)">
              <path
                id="Line_624"
                d="M4.875 0L0 4.875"
                className="cls-2"
                transform="translate(4.875)"
              />
              <path id="Line_625" d="M4.875 4.875L0 0" className="cls-2" />
            </g>
          </g>
        </>
      );

    case "close":
      return (
        <>
          <defs>
            <style>
              {`.closeSvgIcon{fill:none;stroke:#919ca9;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.5px}`}
            </style>
          </defs>
          <g
            id="prefix__Group_5924"
            data-name="Group 5924"
            transform="translate(-498.5 -88.5)"
          >
            <path
              id="prefix__Rectangle_3207"
              d="M0 0H24V24H0z"
              data-name="Rectangle 3207"
              transform="translate(499 89)"
              style={{ opacity: 0, fill: "none", stroke: "#919ca9" }}
            />
            <g
              id="prefix__Group_4518"
              data-name="Group 4518"
              transform="translate(203.177 -580.206)"
            >
              <path
                id="prefix__Line_622"
                d="M13 0L0 13"
                className="closeSvgIcon"
                data-name="Line 622"
                transform="translate(301.324 674.594)"
              />
              <path
                id="prefix__Line_623"
                d="M13 13L0 0"
                className="closeSvgIcon"
                data-name="Line 623"
                transform="translate(301.324 674.594)"
              />
            </g>
          </g>
        </>
      );
    case "create":
      return (
        <>
          <defs>
            <style>
              {`.createSvgIcon{fill:none;stroke:#29263d;stroke-linecap:round;stroke-linejoin:round}`}
            </style>
          </defs>
          <g id="Group_145420" transform="translate(-522.5 -88.5)">
            <path
              id="Line_619"
              d="M10.667 0L0 0"
              className="createSvgIcon"
              transform="translate(525.667 97.022)"
              style={{ stroke: props.stroke }}
            />
            <path
              id="Line_620"
              d="M0 10.667L0 0"
              className="createSvgIcon"
              transform="translate(531 91.688)"
              style={{ stroke: props.stroke }}
            />
          </g>
        </>
      );

    default:
      return <path />;
  }
};

const SVGIcon = ({
  name = "",
  style = {},
  fill = "",
  viewBox = "",
  width = "100%",
  className = "",
  height = "100%",
  id = "",
  stroke = "",
  opacity = "",
  onClick = () => {},
}) => (
  <svg
    width={width}
    style={style}
    height={height}
    className={className}
    xmlns="http://www.w3.org/2000/svg"
    viewBox={viewBox || getViewBox(name)}
    xmlnsXlink="http://www.w3.org/1999/xlink"
    id={id}
    onClick={onClick}
  >
    {getPath(name, { fill, stroke, opacity })}
  </svg>
);

export default SVGIcon;
