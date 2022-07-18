#!/bin/python3

import json
import os
import re
import sys
import urllib.request

import gspread
from dotenv import load_dotenv
from git.cmd import Git

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if __name__ == "__main__":
    with open("service_account.json") as f:
        f.write(os.getenv("SERVICE_ACCOUNT"))  # type: ignore

    gc = gspread.service_account()

    sheet = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1cwZesVrMlr4fQOdHXWJ9_q2VCY7njD2agWynAsDl4_s"
    )
    baja_worksheet = sheet.get_worksheet(0)
    jacon_worksheet = sheet.get_worksheet(1)

    baja_records: list[dict[str, str]] = baja_worksheet.get_all_records()
    jacon_records: list[dict[str, str]] = jacon_worksheet.get_all_records()

    # Create empty dictionaries to make a proper dictionary with the records
    baja = {}
    jacon = {}

    # Take a record and move the id key outside of it
    for record in baja_records:
        baja[record.pop("id")] = record

    for record in jacon_records:
        jacon[record.pop("id")] = record

    bundle = {"baja": baja, "jacon": jacon}

    with open("../data.json", "w") as f:
        json.dump(bundle, f, indent=2)

    git = Git("..")
    git.add("-A")
    git.commit("-m", "Automatic update of data.json")
    git.push(f"https://{GITHUB_TOKEN}@github.com/go-kawaba/diomawe.git")
