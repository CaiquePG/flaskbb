# Baseline de Testes e Cobertura

## Ambiente utilizado

- Sistema operacional: Windows
- Python: 3.13.3
- Pytest: 9.0.3
- Execução realizada com pytest sem paralelismo (`-n 0`)

## Resultado da suíte original

A suíte de testes original do FlaskBB foi executada antes de qualquer alteração no código.

Resultado obtido:

- 231 testes aprovados
- 1 teste ignorado (skipped)
- 1 teste com falha

O teste que apresentou falha foi:

`tests/unit/utils/test_translations.py::test_flaskbbdomain_translations`

A falha ocorre porque o teste espera uma instância de `babel.support.Translations`, porém o ambiente retorna uma instância de `babel.support.NullTranslations`.

A falha foi reproduzida tanto na execução completa quanto na execução isolada do teste. Como ela já estava presente antes das alterações deste projeto, o teste original não foi modificado.

## Cobertura inicial global

A execução da suíte com cobertura apresentou cobertura global inicial de 24%.

- Statements: 6815
- Missing: 5148
- Coverage: 24%

## Cobertura inicial dos módulos

| Módulo | Statements | Missing | Cobertura |
|---|---:|---:|---:|
| `flaskbb/forum` | 1272 | 855 | 33% |
| `flaskbb/management` | 837 | 774 | 8% |
| `flaskbb/user` | 560 | 388 | 31% |

## Módulo escolhido

O módulo escolhido para ampliação da suíte de testes foi `flaskbb/forum`.

A escolha foi baseada na importância do módulo para as funcionalidades centrais do fórum e na existência de trechos com baixa cobertura. Em particular, `flaskbb/forum/views.py` apresentou apenas 7% de cobertura inicial, enquanto `flaskbb/forum/models.py` apresentou 58%.

Dessa forma, novos testes podem explorar cenários ainda não cobertos e aumentar a segurança para as etapas posteriores de refatoração.