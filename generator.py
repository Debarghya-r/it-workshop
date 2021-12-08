import os
import time
from util import prepDir
from util import _FILE_PREFIX_
from util import _FILE_PREFIX_LEN_

src_txt_directory = "./assets/papers/IJCNLP/txt/"
final_txt_out_directory = "./assets/final_out/"


def lintSummary(summary: str) -> str:
    # some linting
    summary = summary.strip()
    if len(summary) != 0:
        if summary.strip()[0] == '\n':
            summary = f"{summary[1:]}"

    summary = summary.replace("\n", "\n\t\t")
    return summary


def getSummary(_lines: list[str], _table_no, _paper_no) -> str:
    abstractive_summary: str = ""
    extractive_sumary: list[str] = []
    full_summary: str = ""
    isTablePresent: bool = False
    full_summary += f"<Paper ID={_paper_no}> <Table ID ={_table_no}>\n"

    for line in _lines:
        search_str: str = f"Table {_table_no}"
        search_str_len = len(search_str)
        index = line.find(search_str)
        if index != -1:
            isTablePresent = True
            if(search_str_len + index + 1 > len(line)):
                continue
            next_char = line[index + len(search_str)]
            if next_char == ":":
                abstractive_summary += line
            else:
                extractive_sumary.append(line)

    if isTablePresent:
        full_summary += f"\t<Abstractive Summary> =\n\t\t{lintSummary(abstractive_summary)}\n\t</Abstractive Summary>\n"
        for ext_sum in extractive_sumary:
            full_summary += f"\t<Extractive Summary> =\n\t\t{lintSummary(ext_sum)}\n\t</Extractive Summary>\n"
        full_summary += f"</Paper ID={_paper_no}>\n\n\n"
    else:
        full_summary = ""

    return full_summary


def parseFile(txt_file_name) -> str:
    suffix = txt_file_name[txt_file_name.index(
        f"{_FILE_PREFIX_}") + _FILE_PREFIX_LEN_: txt_file_name.index(".txt")]
    src_txt_file_path = os.path.join(
        src_txt_directory, f"{_FILE_PREFIX_}{suffix}.txt")
    output_text_buffer: str = ""

    if os.path.isfile(src_txt_file_path):
        with open(src_txt_file_path, "r", encoding="utf-8") as src_txt_file:
            lines = src_txt_file.read().split(".")
            text = ""
            for line in lines:
                line = line.strip() + "."
                text += f"A Line:\n {line}\n"

            for table_no in range(1, 100):
                summary: str = getSummary(
                    lines, table_no, suffix)
                if summary == "":
                    break
                else:
                    output_text_buffer += summary

    return output_text_buffer


def compare(item: str) -> int:
    suffix1 = int(item[item.index(
        f"{_FILE_PREFIX_}") + _FILE_PREFIX_LEN_:item.index(".txt")])

    return suffix1


def parseAllFiles() -> None:
    files_to_parse: list[str] = os.listdir(src_txt_directory)
    files_to_parse: list[str] = sorted(
        files_to_parse, key=compare)
    output_text_buffer: str = ""

    for file in files_to_parse:
        output_text_buffer += parseFile(file)

    #output_text_buffer += parseFile("doc7.txt")

    with open(final_txt_out_directory + "output.txt", "w", encoding="utf-8") as final_txt_out_file:
        final_txt_out_file.write(output_text_buffer)


def parse() -> None:
    prepDir([final_txt_out_directory])

    print("Generating the final Text Output File....")

    start_time = time.time()
    parseAllFiles()
    end_time = time.time()

    print(f"Papers Converted in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    parse()
