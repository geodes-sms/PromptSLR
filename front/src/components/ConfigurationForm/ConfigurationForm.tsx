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
  inclusion: boolean;
  setInclusion: (value: boolean) => void;
  exclusion: boolean;
  setExclusion: (value: boolean) => void;
  inclusionCondition: string;
  setInclusionCondition: (value: string) => void;
  exclusionCondition: string;
  setExclusionCondition: (value: string) => void;
  inclusionCriteria: never[];
  setInclusionCriteria: (value: never[]) => void;
  exclusionCriteria: never[];
  setExclusionCriteria: (value: never[]) => void;
  renderForm: (formFields: Array<any>, className?: string) => JSX.Element;
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
    inclusion,
    setInclusion,
    exclusion,
    setExclusion,
    inclusionCondition,
    setInclusionCondition,
    exclusionCondition,
    setExclusionCondition,
    inclusionCriteria,
    setInclusionCriteria,
    exclusionCriteria,
    setExclusionCriteria,
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
    {
      label: "Number of Classes",
      value: outputClasses,
      setValue: setOutputClasses,
      type: "textInput",
      props: {
        type: "number",
        min: 0,
      },
    },
  ];
  const checkboxForm = [
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

  const inclusionSelectionCriteriaForm = [
    {
      label: "Inclusion",
      value: inclusion,
      setValue: setInclusion,
      type: "checkbox",
    },
    {
      label: "Inclusion Condition",
      value: inclusionCondition,
      setValue: setInclusionCondition,
      type: "dropdown",
      options: ["all", "any"],
      props: {
        disabled: !inclusion,
      },
    },
    {
      title: "Inclusion Criteria",
      value: inclusionCriteria,
      setValue: setInclusionCriteria,
      type: "addableInputs",
      props: {
        onlyValue: true,
        hideInputLabels: true,
        disabled: !inclusion,
        className: "addable-texts",
      },
    },
  ];

  const exclusionSelectionCriteriaForm = [
    {
      label: "Exclusion",
      value: exclusion,
      setValue: setExclusion,
      type: "checkbox",
    },
    {
      label: "Exclusion Condition",
      value: exclusionCondition,
      setValue: setExclusionCondition,
      type: "dropdown",
      options: ["all", "any"],
      props: {
        disabled: !exclusion,
      },
    },
    {
      title: "Exclusion Criteria",
      value: exclusionCriteria,
      setValue: setExclusionCriteria,
      type: "addableInputs",
      props: {
        onlyValue: true,
        hideInputLabels: true,
        disabled: !exclusion,
        className: "addable-texts",
      },
    },
  ];

  return (
    <>
      {renderForm(firstRowForm)}
      {renderForm(checkboxForm)}
      <div className="selection-criteria-section">
        <p className="selection-criteria-section__title">
          {"Selection Criteria"}
        </p>
        {renderForm(inclusionSelectionCriteriaForm, "criteria-form")}
        {renderForm(exclusionSelectionCriteriaForm, "criteria-form")}
      </div>
    </>
  );
};

export default ConfigurationForm;
