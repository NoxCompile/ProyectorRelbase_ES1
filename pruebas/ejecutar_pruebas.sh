#!/usr/bin/env bash
# Genera pruebas/evidencia_pruebas.txt con tu propio servidor (tokens TRUNCADOS).
# Requisitos: servidor corriendo y `python manage.py crear_roles` ya ejecutado.
# Uso (desde la carpeta raíz del proyecto):
#   source <(grep -E '^PASS_' .env | sed 's/^/export /') && bash pruebas/ejecutar_pruebas.sh
BASE="${BASE:-http://127.0.0.1:8000/api}"
OUT="$(dirname "$0")/evidencia_pruebas.txt"
J='Content-Type: application/json'

for v in PASS_ADMIN PASS_NORMAL PASS_VIEWER; do
  [ -z "${!v}" ] && { echo "Falta la variable $v (revisa tu .env)"; exit 1; }
done

token() { curl -s -X POST -H "$J" -d "{\"username\":\"$1\",\"password\":\"$2\"}" "$BASE/token/" \
          | python3 -c "import sys,json;print(json.load(sys.stdin)['access'])"; }
TA=$(token admin_api "$PASS_ADMIN"); TN=$(token normal_api "$PASS_NORMAL"); TV=$(token viewer_api "$PASS_VIEWER")
[ -z "$TA" ] || [ -z "$TN" ] || [ -z "$TV" ] && { echo "No se pudo obtener algún token: ¿corriste crear_roles?"; exit 1; }

limpiar() { tr -d '\r' | grep -vi '^date:\|^server:\|^cross-origin\|^referrer\|^x-\|^vary:' \
  | sed -E 's/eyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/eyJhbGci...(truncado)/g'; }
caso() { { echo; echo "=== $1 ==="; shift; curl -si "$@" | limpiar; echo; } >> "$OUT"; }

: > "$OUT"
echo "Evidencia generada el $(date '+%Y-%m-%d %H:%M') · tokens truncados" >> "$OUT"

caso "1. POST /token/ · 200 OK (se muestra sin claves)" -X POST -H "$J" -d "{\"username\":\"admin_api\",\"password\":\"***\"}" "$BASE/token/" >/dev/null
{ echo; echo "=== 1. POST /token/ · 200 OK ==="; echo '{"refresh":"eyJhbGci...(truncado)","access":"eyJhbGci...(truncado)"}'; } >> "$OUT"
# (se reescribe el bloque 1 arriba para no guardar ni tokens ni claves)
python3 - "$OUT" <<'PY'
import sys,re
p=sys.argv[1]; t=open(p).read()
t=re.sub(r"\n=== 1\. POST /token/ · 200 OK \(se muestra sin claves\) ===.*?(?=\n=== 1\. POST)", "", t, flags=re.S)
open(p,"w").write(t)
PY
caso "2. GET /registros/ · 401 sin token"                       "$BASE/registros/"
caso "3. POST /registros/ · 201 (normal; manda estado=Optimo y la regla lo ignora)" -X POST -H "Authorization: Bearer $TN" -H "$J" -d '{"producto":"Gasas","stock_actual":2,"ventas_esperadas":10,"estado":"Optimo"}' "$BASE/registros/"
ID=$(grep -o '"id":[0-9]*' "$OUT" | tail -1 | cut -d: -f2)
caso "4. POST /registros/ · 400 (stock negativo)"               -X POST -H "Authorization: Bearer $TN" -H "$J" -d '{"producto":"Cable","stock_actual":-2,"ventas_esperadas":5}' "$BASE/registros/"
caso "5. GET /registros/ · 200 lista paginada (viewer)"         -H "Authorization: Bearer $TV" "$BASE/registros/"
caso "6. GET /registros/?estado=Critico · 200 filtro (viewer)"  -H "Authorization: Bearer $TV" "$BASE/registros/?estado=Critico"
caso "7. GET /registros/?estado=Nada · 400 filtro inválido"     -H "Authorization: Bearer $TV" "$BASE/registros/?estado=Nada"
caso "8. GET /registros/$ID/ · 200 detalle"                     -H "Authorization: Bearer $TV" "$BASE/registros/$ID/"
caso "9. POST /registros/ · 403 (viewer solo lee)"              -X POST -H "Authorization: Bearer $TV" -H "$J" -d '{"producto":"X","stock_actual":1,"ventas_esperadas":1}' "$BASE/registros/"
caso "10. PATCH /registros/$ID/ · 403 (normal no edita)"        -X PATCH -H "Authorization: Bearer $TN" -H "$J" -d '{"stock_actual":1000}' "$BASE/registros/$ID/"
caso "11. PATCH /registros/$ID/ · 200 (admin; el estado se recalcula)" -X PATCH -H "Authorization: Bearer $TA" -H "$J" -d '{"stock_actual":1000}' "$BASE/registros/$ID/"
caso "12. DELETE /registros/$ID/ · 403 (normal no borra)"       -X DELETE -H "Authorization: Bearer $TN" "$BASE/registros/$ID/"
caso "13. DELETE /registros/$ID/ · 204 (admin; borrado lógico)" -X DELETE -H "Authorization: Bearer $TA" "$BASE/registros/$ID/"
caso "14. GET /registros/$ID/ · 404 (ya borrado lógicamente)"   -H "Authorization: Bearer $TV" "$BASE/registros/$ID/"
echo "Listo: $OUT"
