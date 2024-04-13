import React from "react";
import "./styles.scss";

const ConfigurationForm = (props: {
  features: string[];
  setFeatures: (value: string[]) => void;
  linient: boolean;
  setLinient: (value: boolean) => void;
  positiveShots: number;
  setPositiveShots: (value: number) => void;
  negativeShots: number;
  setNegativeShots: (value: number) => void;
  renderForm: (formFields: Array<any>) => JSX.Element;
}) => {
  const {
    features,
    setFeatures,
    linient,
    setLinient,
    positiveShots,
    setPositiveShots,
    negativeShots,
    setNegativeShots,
    renderForm,
  } = props;
  const firstRowForm = [
    {
      label: "Features",
      items: ["title", "abstract", "keywords", "authors", "venue", "bibtex"],
      value: features,
      setValue: (value: string[]) => setFeatures(value),
      type: "multi-select",
    },
    {
      label: "Linient",
      value: linient,
      setValue: setLinient,
      type: "checkbox",
    },
  ];
  const secondRowForm = [
    {
      label: "Positive Shots",
      value: positiveShots,
      setValue: setPositiveShots,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
      },
    },
    {
      label: "Negative Shots",
      value: negativeShots,
      setValue: setNegativeShots,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
      },
    },
  ];

  return (
    <>
      {renderForm(firstRowForm)}
      {renderForm(secondRowForm)}
    </>
  );
};

export default ConfigurationForm;
