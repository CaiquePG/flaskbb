from unittest.mock import Mock, patch

import pytest

from flaskbb.forum.views import MarkdownPreview, Search


def test_search_get_renderiza_formulario(application):
    view = Search()

    with application.test_request_context("/search"):
        with patch("flaskbb.forum.views.render_template") as render:
            resultado = view.get()

            render.assert_called_once()
            assert render.call_args.args[0] == "forum/search_form.html"
            assert resultado == render.return_value


def test_search_post_formulario_valido(application):
    view = Search()
    form = Mock()
    form.validate_on_submit.return_value = True
    form.get_results.return_value = ["resultado"]

    view.form = Mock(return_value=form)

    with application.test_request_context("/search", method="POST"):
        with patch("flaskbb.forum.views.render_template") as render:
            resultado = view.post()

            form.validate_on_submit.assert_called_once()
            form.get_results.assert_called_once()
            render.assert_called_once_with(
                "forum/search_result.html",
                form=form,
                result=["resultado"],
            )
            assert resultado == render.return_value


def test_search_post_formulario_invalido(application):
    view = Search()
    form = Mock()
    form.validate_on_submit.return_value = False

    view.form = Mock(return_value=form)

    with application.test_request_context("/search", method="POST"):
        with patch("flaskbb.forum.views.render_template") as render:
            resultado = view.post()

            form.validate_on_submit.assert_called_once()
            form.get_results.assert_not_called()
            render.assert_called_once_with(
                "forum/search_form.html",
                form=form,
            )
            assert resultado == render.return_value


@pytest.mark.parametrize("mode", [None, "nonpost"])
def test_markdown_preview_renderiza_conteudo(application, mode):
    view = MarkdownPreview()

    with application.test_request_context(
        "/markdown",
        method="POST",
        data="Texto de teste",
    ):
        renderer = Mock(return_value="conteudo renderizado")

        with (
            patch(
                "flaskbb.forum.views.make_renderer",
                return_value=renderer,
            ) as make_renderer,
            patch(
                "flaskbb.forum.views.pluggy.hook.flaskbb_load_post_markdown_class",
                return_value=["post"],
            ),
            patch(
                "flaskbb.forum.views.pluggy.hook.flaskbb_load_nonpost_markdown_class",
                return_value=["nonpost"],
            ),
        ):
            resultado = view.post(mode)

            assert resultado == "conteudo renderizado"
            renderer.assert_called_once_with("Texto de teste")
            make_renderer.assert_called_once()

def test_view_forum_redireciona_forum_externo(application):
    from flaskbb.forum.views import ViewForum

    forum = Mock()
    forum.external = "https://example.com"

    with application.test_request_context("/forum/1"):
        with (
            patch(
                "flaskbb.forum.views.Forum.get_forum",
                return_value=(forum, None),
            ),
            patch("flaskbb.forum.views.real"),
        ):
            resultado = ViewForum().get(1)

            assert resultado.status_code == 302
            assert resultado.location == "https://example.com"


def test_lock_topic_bloqueia_e_salva(application):
    from flaskbb.forum.views import LockTopic

    topic = Mock()
    topic.url = "/topic/1"

    with application.test_request_context("/topic/1/lock", method="POST"):
        with patch(
            "flaskbb.forum.views.first_or_404",
            return_value=topic,
        ):
            resultado = LockTopic().post(1)

            assert topic.locked is True
            topic.save.assert_called_once()
            assert resultado.status_code == 302
            assert resultado.location.endswith("/topic/1")


def test_unlock_topic_desbloqueia_e_salva(application):
    from flaskbb.forum.views import UnlockTopic

    topic = Mock()
    topic.url = "/topic/1"

    with application.test_request_context("/topic/1/unlock", method="POST"):
        with patch(
            "flaskbb.forum.views.first_or_404",
            return_value=topic,
        ):
            resultado = UnlockTopic().post(1)

            assert topic.locked is False
            topic.save.assert_called_once()
            assert resultado.status_code == 302
            assert resultado.location.endswith("/topic/1")


def test_raw_post_formata_conteudo(application):
    from flaskbb.forum.views import RawPost

    post = Mock()
    post.username = "usuario_teste"
    post.content = "conteudo_teste"

    with application.test_request_context("/post/1/raw"):
        with (
            patch(
                "flaskbb.forum.views.first_or_404",
                return_value=post,
            ),
            patch(
                "flaskbb.forum.views.format_quote",
                return_value="conteudo_formatado",
            ) as format_quote,
        ):
            resultado = RawPost().get(1)

            format_quote.assert_called_once_with(
                username="usuario_teste",
                content="conteudo_teste",
            )
            assert resultado == "conteudo_formatado"
def test_highlight_topic_destaca_e_salva(application):
    from flaskbb.forum.views import HighlightTopic

    topic = Mock()
    topic.url = "/topic/1"

    with application.test_request_context("/topic/1/highlight", method="POST"):
        with patch(
            "flaskbb.forum.views.first_or_404",
            return_value=topic,
        ):
            resultado = HighlightTopic().post(1)

            assert topic.important is True
            topic.save.assert_called_once()
            assert resultado.status_code == 302
            assert resultado.location.endswith("/topic/1")


def test_trivialize_topic_remove_destaque_e_salva(application):
    from flaskbb.forum.views import TrivializeTopic

    topic = Mock()
    topic.url = "/topic/1"

    with application.test_request_context("/topic/1/trivialize", method="POST"):
        with patch(
            "flaskbb.forum.views.first_or_404",
            return_value=topic,
        ):
            resultado = TrivializeTopic().post(1)

            assert topic.important is False
            topic.save.assert_called_once()
            assert resultado.status_code == 302
            assert resultado.location.endswith("/topic/1")

@pytest.mark.parametrize(
    "sort_by, order_by, expected_sort",
    [
        ("reg_date", "asc", "id"),
        ("post_count", "desc", "post_count"),
        ("username", "asc", "username"),
    ],
)
def test_member_list_opcoes_ordenacao(
    application, sort_by, order_by, expected_sort
):
    from flaskbb.forum.views import MemberList

    with application.test_request_context(
        f"/memberlist?sort_by={sort_by}&order_by={order_by}&page=2"
    ):
        page, order_func, sort_obj = MemberList().get_sorting_options()

        assert page == 2
        assert order_func.__name__ == order_by
        assert sort_obj.key == expected_sort