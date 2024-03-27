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

    case "minus":
      return (
        <>
          <path d="M0 10h24v4h-24z" style={{ fill: props.fill }} />
        </>
      );
    case "plus":
      return (
        <path
          d="M24 10h-10v-10h-4v10h-10v4h10v10h4v-10h10z"
          style={{ fill: props.fill }}
        />
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
