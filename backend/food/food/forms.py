# Most of the Budget and save logic will go here


import pandas as pd
from django.http import JsonResponse, HttpResponseBadRequest
from .utils import get_kroger_access_token
from .utils import fetch_kroger_products

client_id = 'nazeerahmad-243261243034247534474c336551586966456b514e4b694b774e494f2e684e65387571744149726d5576744773567a74486b6e434b314b3371466b4b8212988171852896486'

secret_kroger_key = 'aocx6Pr1qFFN6ZxBe-QfOGBnmeQVClClGHaW89A1'

token = get_kroger_access_token(client_id, secret_kroger_key)

# acess_token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYXBpLWNlLmtyb2dlci5jb20vdjEvLndlbGwta25vd24vandrcy5qc29uIiwia2lkIjoidnl6bG52Y3dSUUZyRzZkWDBzU1pEQT09IiwidHlwIjoiSldUIn0.eyJhdWQiOiJuYXplZXJhaG1hZC0yNDMyNjEyNDMwMzQyNDc1MzQ0NzRjMzM2NTUxNTg2OTY2NDU2YjUxNGU0YjY5NGI3NzRlNDk0ZjJlNjg0ZTY1Mzg3NTcxNzQ0MTQ5NzI2ZDU1NzY3NDQ3NzM1NjdhNzQ0ODZiNmU0MzRiMzE0YjMzNzE0NjZiNGI4MjEyOTg4MTcxODUyODk2NDg2IiwiZXhwIjoxNzQ1MDIzNzY3LCJpYXQiOjE3NDUwMjE5NjIsImlzcyI6ImFwaS1jZS5rcm9nZXIuY29tIiwic3ViIjoiZjk0NmZjYjgtNGVhZS01YmRhLWFjYTAtNGI3YWMyMDQ0NTc4Iiwic2NvcGUiOiIiLCJhdXRoQXQiOjE3NDUwMjE5Njc2NjQ5MzA4MTIsImF6cCI6Im5hemVlcmFobWFkLTI0MzI2MTI0MzAzNDI0NzUzNDQ3NGMzMzY1NTE1ODY5NjY0NTZiNTE0ZTRiNjk0Yjc3NGU0OTRmMmU2ODRlNjUzODc1NzE3NDQxNDk3MjZkNTU3Njc0NDc3MzU2N2E3NDQ4NmI2ZTQzNGIzMTRiMzM3MTQ2NmI0YjgyMTI5ODgxNzE4NTI4OTY0ODYifQ.ItieGcDoYjGgdsxtbgTZxlM3GM6XwZx73UWevcRYTX9-fanGGE2_Vad5BQhlwLyQyC4xT3C6eBt4fjzc8W8U3h8T8VFa2SsOQDCt0DFN7LX0MKc2-VmrCJnSh8Hqb-ls5nOywdMTFpxpXJ32B9VQDRwsEmE9BgQd8n2MLaO-b8eCiqYF9HXoZLTBspmz6KaHWfaLPEMaIzDRgqSYtdnWQ46G5ffUyvhQmkaxH1hEFBWPC2wRQsku2x3fC07RLKgQa7lGYQKV0iibCZ6ap_11t9MSMNBxuOvdWBinccoii3m7zgTIgmyTsL0J6N5uKjwLfVdpuKbd0xkWrWyybj28yg'

access_token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYXBpLWNlLmtyb2dlci5jb20vdjEvLndlbGwta25vd24vandrcy5qc29uIiwia2lkIjoidnl6bG52Y3dSUUZyRzZkWDBzU1pEQT09IiwidHlwIjoiSldUIn0.eyJhdWQiOiJuYXplZXJhaG1hZC0yNDMyNjEyNDMwMzQyNDc1MzQ0NzRjMzM2NTUxNTg2OTY2NDU2YjUxNGU0YjY5NGI3NzRlNDk0ZjJlNjg0ZTY1Mzg3NTcxNzQ0MTQ5NzI2ZDU1NzY3NDQ3NzM1NjdhNzQ0ODZiNmU0MzRiMzE0YjMzNzE0NjZiNGI4MjEyOTg4MTcxODUyODk2NDg2IiwiZXhwIjoxNzQ1MDI5MTUyLCJpYXQiOjE3NDUwMjczNDcsImlzcyI6ImFwaS1jZS5rcm9nZXIuY29tIiwic3ViIjoiZjk0NmZjYjgtNGVhZS01YmRhLWFjYTAtNGI3YWMyMDQ0NTc4Iiwic2NvcGUiOiIiLCJhdXRoQXQiOjE3NDUwMjczNTI4MjY5NTcwMzgsImF6cCI6Im5hemVlcmFobWFkLTI0MzI2MTI0MzAzNDI0NzUzNDQ3NGMzMzY1NTE1ODY5NjY0NTZiNTE0ZTRiNjk0Yjc3NGU0OTRmMmU2ODRlNjUzODc1NzE3NDQxNDk3MjZkNTU3Njc0NDc3MzU2N2E3NDQ4NmI2ZTQzNGIzMTRiMzM3MTQ2NmI0YjgyMTI5ODgxNzE4NTI4OTY0ODYifQ.luE3HmhDcMYYyPA1bGquqheUoIGPI899SbCCNeiYmH88YUg5X00Ra45Qpe4udEPiHQOh2IKZxPxqcwCOYDTSePdtFQEE8vEye_U_P1eP2s3kr1DP2GVV9pP7MivzMy1UOi73JKsnpZk0AS7VjPvaRdy8Ycj00KgN-Mvn7-WfsMEwzIPWnlus86GqerGZp1CFtPXjJUSv4kTr7gOZ7CUn9KlUMcLKTUxRl4JRVFE97dX5NpqRplJI8B0n7nhTYdR11ajAPTyhUTke_Erhsod04RvCbcxl1pBUiQRBfZisL-G67z33owid8xHomZFTfLn7A1YUa0b6trxDQcBfYZqK8A'


def KrogerFoodView(request, query):
    if request.method != 'GET':
        return HttpResponseBadRequest("Only GET requests are allowed.")

    try:
        location_id = request.GET.get('locationId', '00858000')
        items = fetch_kroger_products(query, location_id)
        return JsonResponse({"items": items})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def filter_items_with_pandas(items, budget=None, keyword=None):
    if not items:
        return []

    cleaned = []
    for item in items:
        price = item.get("items", [{}])[0].get("price", {}).get("regular")
        if price:
            cleaned.append({
                "description": item.get("description", "").lower(),
                "price": price,
                "item": item
            })

    df = pd.DataFrame(cleaned)

    if budget:
        df = df[df["price"] <= budget]

    if keyword:
        df = df[df["description"].str.contains(keyword.lower())]

    df = df.sort_values("price")

    return df["item"].tolist()
