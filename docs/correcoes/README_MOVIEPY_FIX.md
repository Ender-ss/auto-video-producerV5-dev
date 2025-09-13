# Guia Completo para Resolver o Problema do MoviePy

## Status Atual da Instalação

Após as verificações, identificamos que:

✅ **MoviePy está instalado**: Versão 2.1.2
✅ **Dependências básicas do MoviePy estão funcionando**: Imageio, NumPy, Pillow/PIL
❌ **Importação do moviepy.editor falha**: Erro 'No module named 'moviepy.editor''
⚠️ **Python tem problemas de configuração**: Mensagem 'Could not find platform independent libraries <prefix>'
⚠️ **FFmpeg não está instalado ou configurado corretamente**

## Solução Passo a Passo

### 1. Corrija a Instalação do Python

O erro 'Could not find platform independent libraries <prefix>' indica problemas graves com a instalação do Python. Recomendamos:

- **Reinstale o Python do zero**: Baixe a versão mais recente do [site oficial do Python](https://www.python.org/downloads/)
- **Marque a opção 'Add Python to PATH'** durante a instalação
- **Verifique a instalação**: Abra um novo terminal e execute:
  ```
  python --version
  pip --version
  ```

### 2. Instale o FFmpeg (Requerido pelo MoviePy)

O MoviePy depende do FFmpeg para processar vídeos e áudios:

1. Baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html)
2. Extraia o arquivo zip para uma pasta no disco rígido (ex: `C:\ffmpeg`)
3. Adicione a pasta `bin` do FFmpeg ao PATH do sistema:
   - Pressione Windows + R, digite `sysdm.cpl` e pressione Enter
   - Na aba 'Avançado', clique em 'Variáveis de Ambiente'
   - Selecione 'Path' na seção 'Variáveis do sistema' e clique em 'Editar'
   - Clique em 'Novo' e adicione o caminho para a pasta bin (ex: `C:\ffmpeg\bin`)
4. Reinicie o computador para que as alterações tenham efeito
5. Verifique a instalação abrindo um novo terminal e executando:
   ```
   ffmpeg -version
   ```

### 3. Reinstale o MoviePy após corrigir o Python e instalar o FFmpeg

Abra um novo terminal com permissões de administrador e execute:

```
python -m pip install --upgrade moviepy
```

### 4. Verifique se a correção no código da pipeline já está aplicada

Nossa análise mostrou que a função `set_audio` no arquivo `video_creation_service.py` deve ser substituída por `with_audio` para funcionar com a versão atual do MoviePy.

Para verificar se a correção já está aplicada, execute:

```
findstr /C:"with_audio" /C:"set_audio" backend\services\video_creation_service.py
```

Se `set_audio` ainda estiver presente, edite o arquivo manualmente e substitua todas as ocorrências por `with_audio`.

### 5. Reinicie a Pipeline

Após concluir todas as etapas acima, reinicie a execução da pipeline:

```
cd backend
python app.py
```

## Solução Alternativa: Usar um Ambiente Virtual

Caso continue enfrentando problemas, recomendamos usar um ambiente virtual Python:

```
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install moviepy
```

## Verificação Final

Crie um arquivo `test_final.py` com o seguinte conteúdo e execute-o para confirmar que tudo está funcionando:

```python
from moviepy.editor import VideoFileClip
print("Importação do VideoFileClip concluída com sucesso!")
print(f"Método 'with_audio' disponível: {hasattr(VideoFileClip, 'with_audio')}")
print("Verificação concluída!")
```

Execute com:
```
python test_final.py
```

Se a importação for bem-sucedida, sua configuração está correta e a pipeline poderá ser executada normalmente.

## Observações Importantes

- Sempre feche e abra novos terminais após alterar o PATH do sistema
- Certifique-se de ter permissões de administrador para instalar softwares
- O MoviePy 2.1.2 exige que todas as chamadas a `set_audio` sejam substituídas por `with_audio`
- O FFmpeg é uma dependência crítica para o funcionamento do MoviePy

Se você continuar enfrentando problemas, considere reinstalar todo o sistema de desenvolvimento do zero para garantir uma configuração limpa e estável.