from typing import Dict, Union, Any, List
import streamlit as st
from io import StringIO
import io
from uuid import UUID
import time
import os

from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackHandler

from langchain.schema import AgentAction, LLMResult

os.environ["OPENAI_API_KEY"] = "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"

st.set_page_config(layout="wide")
col1, col2 = st.columns(2, gap="small")

stats_map = {'no_of_requests': 0, 'total_time_taken': 0, 'req_time_taken': 0}


class CustomOpenAICallback(BaseCallbackHandler):
    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        stats_map['req_start_time'] = time.time()
        self.print_message(
            f"on_llm_start {stats_map['req_start_time']} and following are the prompts: {prompts}",
        )

    # def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
    #     pprint(f"on_new_token {token}")

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        self.print_message(f"on_llm_error {error}")

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            **kwargs: Any,
    ) -> Any:
        stats_map['req_end_time'] = time.time()
        stats_map['req_time_taken'] = stats_map['req_end_time'] - stats_map['req_start_time']
        stats_map['total_time_taken'] = stats_map['total_time_taken'] + stats_map['req_time_taken']
        self.print_message(f"on_llm_end {stats_map['req_end_time']} and following are the response {response}")

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        self.print_message(f"on_chain_start and inputs are: {inputs}")

    def on_chain_end(
            self,
            outputs: Dict[str, Any],
            *,
            run_id: UUID,
            **kwargs: Any,
    ) -> None:
        self.print_message(f"on_chain_end and inputs are: {outputs}")

    def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        self.print_message(f"on_tool_start and inputs are: {input_str}")

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        self.print_message(f"on_agent_action {action}")

    def print_message(self, message):
        print("DEBUGGER: " + message)


def comment_code(language):
    if uploaded_file is not None:
        i_stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        i_string_data = i_stringio.read()

        llm = OpenAI(temperature=1, max_tokens=-1, callbacks=[CustomOpenAICallback()])

        text = f"Generate {language} docs for the given code and return the generated code\n\n{i_string_data}"

        with get_openai_callback() as cb:
            r1 = llm.invoke(text)
            stats_map['no_of_requests'] = stats_map['no_of_requests'] + 1

        bytesio = io.BytesIO(r1.encode())
        o_stringio = StringIO(bytesio.getvalue().decode("utf-8"))
        r_string_data = o_stringio.read()

        with col1:
            st.subheader(body=':red[Before comments]', help='Before code comments', anchor=False)
            st.code(i_string_data, language=language.lower())

        with col2:
            st.subheader(body=':green[After comments]', help='After code comments', anchor=False)
            st.code(r_string_data, language=language.lower())

        with st.expander(":blue[**Cost Statistics**]"):
            statsCol1, statsCol2, statsCol3, statsCol4, statsCol5, statsCol6 = st.columns(6, gap='small')
            statsCol1.metric(label=":grey[*No of Request*]", value=f"{cb.successful_requests}")
            statsCol2.metric(label=":grey[*Prompt Tokens*]", value=f"{cb.prompt_tokens}")
            statsCol3.metric(label=":grey[*Completion Tokens*]", value=f"{cb.completion_tokens}")
            statsCol4.metric(label=":grey[*Total Tokens*]", value=f"{cb.total_tokens}")
            statsCol5.metric(label=":grey[*Total Cost (USD)*]", value=f"${cb.total_cost:.4f}")
            statsCol6.metric(label=":grey[*Request Time Taken*]", value=f"{stats_map['req_time_taken']:.2f} Secs")


# st.button("Cost Analysis", on_click=showUsage(), help=showUsage())
st.header("Code Comment Generation", divider='blue')
language = st.selectbox('Pick your Language', ['Python', 'Java', 'Kotlin'])
uploaded_file = st.file_uploader("Choose a file")
if st.button(label="Generate Documentation"):
    comment_code(language)
