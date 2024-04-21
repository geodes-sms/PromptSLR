import React from "react";
import "./styles.scss";

const ProjectInfoForm = (props: {
  projectName: string;
  setProjectName: (value: string) => void;
  topicTitle: string;
  setTopicTitle: (value: string) => void;
  topicDescription: string;
  setTopicDescription: (value: string) => void;
  renderForm: (formFields: Array<any>, className?: string) => JSX.Element;
}) => {
  const {
    projectName,
    setProjectName,
    topicTitle,
    setTopicTitle,
    topicDescription,
    setTopicDescription,
    renderForm,
  } = props;

  const formData = [
    {
      label: "Name",
      value: projectName,
      setValue: setProjectName,
      type: "textInput",
      props: {
        placeholder: "myproject",
      },
    },
    {
      label: "Topic Title",
      value: topicTitle,
      setValue: setTopicTitle,
      type: "textInput",
      props: {
        placeholder: "RL4SE",
      },
    },
    {
      label: "Topic Description",
      value: topicDescription,
      setValue: setTopicDescription,
      type: "text-area",
      props: {
        placeholder: "Add an optional description for your topic.",
        rows: 12,
      },
    },
  ];
  return <>{renderForm(formData, "project-info-form")}</>;
};

export default ProjectInfoForm;
