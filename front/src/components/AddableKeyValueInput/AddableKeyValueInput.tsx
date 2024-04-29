import React, { Dispatch, useEffect, useState, SetStateAction } from "react";
import "./styles.scss";
import TextInput from "../TextInput/TextInput";
import SVGIcon from "../SVGIcon/SVGIcon";

const AddableKeyValueInput = (props: {
  title: string;
  values: Array<any>;
  setValues: Dispatch<
    SetStateAction<{ key: string; value: string; id: string }[]>
  >;
  onlyValue?: boolean;
  hideInputLabels?: boolean;
  className?: string;
  disabled?: boolean;
}) => {
  const [data, setData] = useState([
    { key: "", value: "", id: crypto.randomUUID() },
  ]);

  const updateData = (
    updatedIndex: number,
    updatedKey: "key" | "value",
    text: string
  ) => {
    const newData = [...data];
    newData[updatedIndex][updatedKey] = text;
    setData(newData);
  };

  const addField = () => {
    const newData = [...data];
    newData.push({ key: "", value: "", id: crypto.randomUUID() });
    setData(newData);
  };

  const removeField = (index: number) => {
    const newData = [...data];
    newData.splice(index, 1);
    setData(newData);
  };

  useEffect(() => {
    /* tslint:disable */
    props.setValues(data);
  }, [JSON.stringify(data)]);

  const renderKeyValuePairInput = (index: number) => {
    return (
      <div className="addable-inputs__row" key={data[index].id}>
        {!props.onlyValue && (
          <TextInput
            label={props.hideInputLabels ? "" : "Key"}
            value={data[index].key}
            setValue={(text) =>
              props.disabled ? {} : updateData(index, "key", text)
            }
            placeholder={`Key${index + 1}`}
            disabled={props.disabled}
          />
        )}
        <TextInput
          label={props.hideInputLabels ? "" : "Value"}
          value={data[index].value}
          setValue={(text) =>
            props.disabled ? {} : updateData(index, "value", text)
          }
          placeholder={`Value${index + 1}`}
          disabled={props.disabled}
        />
        {data.length > 1 ? (
          <div
            className="addable-inputs__modify-btn"
            onClick={() => (props.disabled ? {} : removeField(index))}
          >
            <SVGIcon name="minus" width={"20"} height={"20"} fill={"#D20F39"} />
          </div>
        ) : null}
        {index === data.length - 1 ? (
          <div
            className="addable-inputs__modify-btn"
            onClick={() => (props.disabled ? {} : addField())}
          >
            <SVGIcon name="plus" width={"20"} height={"20"} fill={"#40A02B"} />
          </div>
        ) : null}
      </div>
    );
  };

  return (
    <div
      className={`addable-inputs ${
        props.disabled && "addable-inputs--disabled"
      } ${props.className}`}
    >
      <p className="addable-inputs__title">{props.title}</p>
      {data.map((item, i) => {
        return renderKeyValuePairInput(i);
      })}
    </div>
  );
};

export default AddableKeyValueInput;
