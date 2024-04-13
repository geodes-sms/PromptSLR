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
  outputClasses: number;
  setOutputClasses: (value: number) => void;
  showReasons: boolean;
  setShowReasons: (value: boolean) => void;
  confidence: boolean;
  setConfidence: (value: boolean) => void;
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
    outputClasses,
    setOutputClasses,
    showReasons,
    setShowReasons,
    confidence,
    setConfidence,
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
  const secondRowForm = [
    {
      label: "Linient",
      value: linient,
      setValue: setLinient,
      type: "checkbox",
    },
    {
      label: "Show Reasons",
      value: showReasons,
      setValue: setShowReasons,
      type: "checkbox",
    },
    {
      label: "Confidence",
      value: confidence,
      setValue: setConfidence,
      type: "checkbox",
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
