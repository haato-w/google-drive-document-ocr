from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
DOC_SCOPES = ['https://www.googleapis.com/auth/documents']


folder_id = '1pTCwh_QLgjShk-tgmoXgbbDnCDKSN3DW'


# 画像ファイルを特定のフォルダにアップロードする
def upload_file(service, file_path):
    fname = file_path.split('/')[-1]
    file_metadata = {
        'name': fname,
        'parents': [folder_id]
    }
    media = MediaFileUpload(
        file_path, 
        mimetype='image/jpeg', 
        resumable=True
    )
    file = service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()

    return file.get('id')


# googledrive内の画像ファイルをdocumentの形式でコピー
def copy_file_as_gdoc(service, file_id):
    dst = {
        'name': file_id + "_copied_document", 
        'mimeType': "application/vnd.google-apps.document"
    }
    doc_file = service.files().copy(
        fileId=file_id, body=dst
        ).execute()

    return doc_file.get('id')


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text


# documentのテキストを読み取る
def extract_text_from_gdoc(doc_service, gdoc_id):
    document = doc_service.documents().get(documentId=gdoc_id).execute()
    doc_content = document.get('body').get('content')
    #print(document.get('title'))
    #print(read_strucutural_elements(doc_content))
    return read_strucutural_elements(doc_content)


# 画像ファイルを削除する
def delete_file(service, file_id):
    file = service.files().delete(
        fileId=file_id
    ).execute()


# googledrive内のファイル一覧を取得する（サンプル）
def get_show_files(service, page_num=10):
    results = service.files().list(
        pageSize=page_num, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def get_drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    """ここから"""
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    """ここまでがポイント！"""

    return service


def get_doc_service():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./client_secret.json', DOC_SCOPES)
        creds = tools.run_flow(flow, store)
    doc_service = build('docs', 'v1', http=creds.authorize(Http()))

    return doc_service


if __name__ == '__main__':
    service = get_drive_service()
    doc_service = get_doc_service()

    # Call the Drive v3 API
    #get_show_files(service)
    file_id = upload_file(service, 'data/sample.jpg')
    print ('File ID: %s' % file_id)
    gdoc_id = copy_file_as_gdoc(service, file_id)
    print ('Gdoc ID: %s' % gdoc_id)
    doc_text = extract_text_from_gdoc(doc_service, gdoc_id)
    print('Doc Text: \n', doc_text)
    delete_file(service, file_id)
    delete_file(service, gdoc_id)
