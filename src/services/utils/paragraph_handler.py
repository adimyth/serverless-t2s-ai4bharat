#! /usr/bin/env python
# encoding: utf-8

import re

non_chars_regex = re.compile(r"[^\w]")


class ParagraphHandler:
    def __init__(self, max_text_len=512):
        self.L = max_text_len

    def split_text(self, text: str, delimiter="."):
        """Splits text at delimiter into paragraphs of max. length self.L"""
        delimiter = " " if delimiter not in text else delimiter
        if delimiter not in text:
            return [text]

        paragraphs = []
        l_pos, r_pos = 0, 0
        while r_pos < len(text):
            r_pos = l_pos + self.L
            if r_pos >= len(text):  # append last paragraph.
                paragraphs.append(text[l_pos : len(text)])
                break
            while (
                delimiter is not None
                and text[r_pos] != delimiter
                and r_pos > l_pos
                and r_pos > 0
            ):  # find nearest delimiter < r_pos to split paragraph at.
                r_pos -= 1
            extracted_paragraph = text[l_pos : r_pos + 1]
            extracted_paragraph_without_special_chars = non_chars_regex.sub(
                "", extracted_paragraph
            )
            if extracted_paragraph_without_special_chars:
                paragraphs.append(extracted_paragraph)
            l_pos = r_pos + 1  # handle next paragraph
        return paragraphs
