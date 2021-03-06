import styled from "styled-components";
import {NoShape} from "../../models/tetromino";

export const StyledCell = styled.div`
  width: auto;
  background: rgba(${props => props.color}, 0.8);
  border: ${props => (props.shape === NoShape.shape ? "0x solid" : "4px solid")}
  border-top-color: rgba(${props => props.color}, 1);
  border-bottom-color: rgba(${props => props.color}, 0.1);
  border-left-color: rgba(${props => props.color}, 0.3);
  border-right-color: rgba(${props => props.color}, 1);
`;
