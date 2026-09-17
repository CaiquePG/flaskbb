"""Funcionalidades principais relacionadas ao fórum.

Este módulo reúne os componentes responsáveis pelas operações centrais
do fórum no FlaskBB, incluindo fóruns, tópicos, posts, pesquisa,
listagem de membros e ações de moderação.

Os principais componentes estão distribuídos entre:

- models.py: entidades e regras relacionadas ao domínio do fórum;
- forms.py: formulários utilizados pelas funcionalidades do fórum;
- views.py: views e fluxos HTTP das operações do fórum;
- utils.py: funções auxiliares utilizadas pelo módulo;
- locals.py: objetos locais utilizados no contexto do fórum.

As funcionalidades deste pacote possuem dependências com outros
componentes do FlaskBB, principalmente usuários, autenticação,
permissões, banco de dados e sistema de plugins.
"""

import logging

logger = logging.getLogger(__name__)
