import pytest
import allure

from common.journal import message_draft_text
from helpers.steps import create_message, create_draft, send_message, send_draft_message, \
    create_message_with_attachment
from initialization import initialization


@pytest.fixture()
def precondition():
    return initialization()


class TestGmail:

    @allure.title('Тест отправки письма')
    @allure.description('В ходе теста создается письмо с переданными параметрами: отправителем, получателем, темой '
                        'письма и текстом письма, после чего происходит отправка созданного письма')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_send_message(self, precondition):
        message = create_message()
        assert message, 'Не удалось создать письмо'

        send = send_message(precondition, message)
        assert send, 'Не удалось отправить письмо'

    @allure.title('Тест отправки письма с использованием черновика')
    @allure.description('В ходе теста создается письмо с переданными параметрами: отправителем, получателем, темой '
                        'письма и текстом письма, созданное письмо сохраняется как черновик, после чего происходит '
                        'отправка созданного письма')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_message_from_draft(self, precondition):
        message = create_message(message_draft_text)
        assert message, 'Не удалось создать сообщение'

        draft_message = create_draft(precondition, message)
        assert draft_message, 'Не удалось создать черновик'

        send = send_draft_message(precondition, draft_message)
        assert send, 'Не удалось отправить письмо'

    @allure.title('Тест отправки письма с вложением {attachment}')
    @allure.description('В ходе теста создается письмо с переданными параметрами: отправителем, получателем, темой '
                        'письма, текстом письма, а также одним из вложений, после чего происходит отправка созданного'
                        ' письма')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('attachment', ['test_image.jpg', 'test_text.txt', 'test_music.mp3', 'test_video.mp4',
                                            'test_doc.docx'])
    def test_send_message_with_attachment(self, attachment, precondition):
        message = create_message_with_attachment(attachment)
        assert message, 'Не удалось создать сообщение с вложением'

        send = send_message(precondition, message)
        assert send, 'Не удалось отправить письмо'
