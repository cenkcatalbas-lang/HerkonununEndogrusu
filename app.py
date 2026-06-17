import streamlit as st
import pandas as pd
import json
import os
import re
import random
import requests

# --- AYARLAR ---
YIGIT_IMG = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCACiAL0DASIAAhEBAxEB/8QAHAAAAgIDAQEAAAAAAAAAAAAAAAcGCAEEBQMC/8QAOhAAAQIFAwEGBAQFAwUAAAAAAQIDAAQFBhEHEiExCBMiQVFhFHGBkTJCobEVFiMzUnKC4SRiotHx/8QAGgEAAgMBAQAAAAAAAAAAAAAAAAMBAgQFBv/EACwRAAICAgECBQMEAwEAAAAAAAABAgMEESESMQUTIkFRYXGhBhSBsSMykdH/2gAMAwEAAhEDEQA/AOrN651yuhEtadtzC3lp8W8Zwcc4MaTdtax3jh2pVD+GSyj/AGlLKSB8hEw7ME7IzlifBCXaROU91TTvhwpQ6gn7/pDcJCQABGpz6eEjN0dXLYkaH2faSlffV6qzVQWTkpCto+/WJ5RNOLMo6AJaiy6lD8zid5/WJctXMeK1RVzbLdEUectLSssgJl5dppI6BCQI+1rOc45j4K8R8FcRojej13Z5JjG/HSPBS88ZjO8YxBohs9e85j6DmI1wo8xqT08xJtFx5wJx0GeTFJzjBdUnwWhGU3qPLOmpzCTkxy6nXpKTSQ66krAyADC2vTUyVpiVpU6EJHROfEYRF66lzlUKm5TeynJyonkxjhfdkPVUdL5N7xqsdbvlz8Fgrr1Kl6e04ozTTASOhOVH5Qq57XCaYdV8GHVnPVa+DCRnJ9+bXvmXVrJ9VGPDJKcnOI0V+HqPNkm2RLxHjpqioot3p7rPTaxIBueWhmZQMFK1Yz8oYNuXVTq2tbcs6guJ6pCsxQVp5aFgoWUkdMGGBo1drtvXlKzD76yw4oNvAnPBjRCnp7MS7a5rTjz8l2AfIcRh1DbqCh1KVpxghQyDHhKTLUzLNzDKgpC0hST6gx6AnPMWSMr2jh1mzLWqqVCdokoskcqSgJP3HMQWv6F2xPIP8NfmKes+QJWPsYa+RAk5HrBoOpiBc0x1EtdPe25XFvIR+Ftp0pJ/29I9Kfqrf9ruFi6aKt9CeAS3sUfqMgw+d3PEfMzLy022W5lht1BGCFpBgZKkvdEKtXWW0q1tbmphVNfPG1/hOfnCg7RN1prl4tMUp7v5STZ2pcaVlJKsE/tDK1K0ys1dvz9TRLimuMMqcCmfCnOOMiF9oPpk7e9GqFSeYV3TT6Wm1KVgK4ycevURST0TpPsdezN+nfaGqttPqWiTqDiu738DxErTj77YsCtXEJ/tl0B2SqdDvmUUpKpdYZdwOqgQpJz/ALSIYVo1tuv2vIVZopImGEqVg9FY5H3iXykw7No663D6x4OLOesYKjn29Y+Fc8iIIPrcTGM+sfIKjzGT0xEgB6dIE8jpGQfCRAMDqMiAjRq1WbRKSinSoAgeZiu2p+qDrUw5KyS97oJSo+Qifa/VaZoVGbnZdtTm4lJx0A9YqjPTjk1PLmVjcVq3cxihju+1ztXpXZG2ORGivVT9T7/Q3Zt+rV2ZU473jzpPnmPtq1K08VBuRcWU9eI9aZdE3TV5ZZa3D1TElpmpVYYV3zlNYWCccJxHWhuPCjtfczaqs5nZp/bZC52g1SVG96UdQEnqUnEcsgJzuBJz9otRpZd9JvJxdIqFJbCyjkOJB/WIJ2h7Ap1vNoqlJSWm1rwpry+kRfbXDW04t/JmcZVy7qS+UJLAznI5jZk1YcB5POeOMRrKPGPIR6S3409eD1ia+5eXYu7oxVG6pYUgtK9ym0BCsnzETXkQtOzvIol7BYcRu/qkqhlDPnBfFRsaREH1R2fWeYMk8AYgA55EZOYSW0Yxg4jPSM844GYOAcmAgUnabuH+H2ixSGSovT7mFJT12Dn/AIhz6FW2i2dMqTIFJDy2g88SMEqVzz9CIrzVgb/7RlOojaiZWQcAXgZBSg7lfviLesoS22ltAwlIAA9oRYx8FwRHWS127u0+qdHWDvU0VtEAZC08jGYr12XLg7ymVC1pkqS/JulbSF8HaT4vsYtqpIUCDyCMRTq/ZQaY9o9ucYaW1TqmoLUonw4cOFfYjpBB+xE17j5KiDgiMEekZStK0haeihkfKMjBHpFyh8Y8sxnEBIzmMgA+0SAAZ4xGH1tsNKWtQSlIySY+nVJQkqzwBkwrdU75Zp0m4224CvolAPJjJkX+XqMVuTNWNj+a9vhLuamstxUyYoUxJO7FpWkpQMck+0JrTXTSeuGopcnGly8mF/iUOSInFh2fPXNUEV24y4GEq3MsHzHuIcLXw0khCW0pQlIwMDpGWOU8R8vbf4NNmPHI9MFpL/r+pXPWfTf+WqhLTEg2tUi6AFEDO0+8bSHbVkbYkmXENPTRUCQOv1h5XBNyNSknZCbQl1laSFA+XyiA25pDR3amJ5yaU7LpVlKPT2jo4eZXZzOWtPf3MtuFdh1tqHUn2+hNLZt+jSNut1ymyCWplTG/w9TxEE1Nqzd6WbMs9ypmYlSVEOeEjH7w55dhEnJIlZcBLbadoHtCF112yrqilBQpw9W+AR7xhysvzr0nvvwOxMVKt7S0l+RBiXWXlNJSVKBxwMx26fa1cmEd4zIPkDnIQTxEvt2h0qn05m4pqZ7xscqbCc8wzrZ1YtpMyxLNFtKVeHxNbcR1YZdeuzbF2+GXJJuSW/k2NBbwZkJNu2KrulplJ/phwYzDwQApIUOh6QhdbJKTmqZL3XSwhLkvg7m+DjOc8Q2dOKwK1achNleXFMp3/PEVqt/cQdq+dGecXBKElp/2SQ8cjrB184wckZjO09TxFhYZx0Ecm76oih2zUKq4R/07Clgep9I6pJxCd7TtZUzQJG35dwh6feBWE9cA4x9yIhglydPscUCYmp6tXnPJyp9fdMKUnnqSo5+0WWiJ6R2+LY09o9IIPetSyS6SMErIyYlkZpPbNKCEP2yLUFVsRu4JWXC52mPJJUD4u7J5+3WHxHLuqks1y3KhSZlCVtzcutog+4IzBF6ZDW0JPR64hcNhSE6tW59pHcvD0UP+Il+/nIivmgdRmLdvis2XPhbOHF902o/mSSP1ABh8ocKvOHtCdG0Dk5HnH1k5jXQogiPdIUUxDDRwL5qiaZQ5iZUspS2nJ94rpa5F3X+mfnVZkml/hV54hidpuoTMnQGJdhRCXl4WB5xBdJZbu6Ip5JSXFKJOOojnzjKuMrX/AAdvwmEcqfkPt3Y+FTkhKSwDO3aE8ARwpiqiYUsDwpjgoL7gCcLziORcNal6PLKLq9zxGENg8kxx5VytnxyekWHRixcpyNu56yzSJZT7igonhCQeVHyiTaULqi6O5NVTwB1W5tBGMCINYFpT911dFaraFokm1BTbSs4JhyPtMMIDLKQlKRgY8o329GJR0LmT7/Q87bl2Z13p4rX5NaqTryE4QRiIVd6JWpU56WeCVLWkjJTyIlk6lW3d5RDqiU/ErJHHlHGjKTmpM72BjQlw0QVVAVSrVm5dIEzuSSEEQspxykfws7WHGJ1K8Y8hD+ZS24kgkHEcS57Ttycp5W6huUd6lzpHcw8hxepe5TxTAVkF5WlpaIfSrkdVpW9S5lwrcWvYjdyduYsFobKrk7Dk0Op2qIKufMQgbFtpdfuVFMk1Fyny68leODFrKXLNSMizKNJCUtICRiPTTojjU6XeT3r4PBztdt2u/Txs3N+T8o+irPBMfAwTGSQOhEYlwX0ffUY6e8Iemy69Qe0qwyle6Qpbm5aSM+FHB/8ALENu+623QbQqNTcVju2SE/6iMD9Yi/YzoLxp1Xu6cSkuzzvdNKx4inqrn/VFJyLwRYpKQkACMwQQgaEYPOYzB6wAU57TNFmLJ1jkbzkmy1KzziVLWFcBQwFDHuIcVMm2p6ny84wQpp9tLiCPQjMe/autL+Z9K5t5lgOzdOPxLOOvHBx9CYXHZrrwrdiCSdcK5inr7tWeu08p/SHxltFHHYz2W93WN9pvaORHmwjB6RuoQCnJgbDpIBrFY/8AOFtOMy/hmmsqa9z6RXSmSV62lNusM019ac8oU2cfOLmpCQMCPhbMu4vK2m1HGMlOYfXbWo9NkNoT0XQn5lM9MqDcd23cxKNlcguQ70hPebMAmGbpnpqmYkpev191U3NPJC0trOQnMdTtCy0uZWlMFtsIXOJHA6cwyqWlmUpUujKUhLSQPtGG62Co3XHp22aYyuvmldLq0arcq3LS6W2WkoSBjAGAI13WEgkqHJjamJ+WKv7qfvGk9PS27BcSPTmOFbFPk7NNc/g0Z1AQwdycjmIVUGQVqKkEJzErqdSlwkgug4hOavXmiUlPgafMD4hSuVtn8IhNNErJ9MUdum9YtbnM492SNxUWZfrVKm3RLg7ltqPAESDTy0azfEmifq84pMnuzsHGY41Cqc/UtN6omtOpWkI/ouH8R9jEx06viRpmnDTIfabUynCju5/+x6jBv/bVSk4pyXCOB4tGWVZFQk4xktvnQzLaoNDthruJMNNk9ScZMd4zKFDKFZits9qJVJ+ZdVSJFyZHkpWc/OO3pxqc/M1hNJq6FNOqVtGfWL13zyHuXc5rqxoLoqnv+B6rfO4AcR6tvDoesc5LmQCOcjgwKXg8qwAMmL6EaFd2mK245KU22JJYVMTjoUUDz5wkfeLGaU283bGn9Io6G0oLUukrCR+c8q/UxV60JZWofaPbOzvpCnud4o54ARyn9RFyUABIAAAHSM83tlorSMwQQRQsEEEEAHhUJZmck3ZV9CVtOoKFJUMggjEU7sJtenfaAq9rv4akp51SGEA+Eg5LZ+2RFyzFaO2RQHZCbol8U5Ox2XeDb6kp56goPH1EWiwGslPpHqgnnH2jkWjWGa9bchV5c5bmmUuD2PmI6pyDDCdApWFdY+VL285jCyPKNWYeCAdxiS0Y7IPrVQ56tUJqZpjffTUo6HUt56xDTqRMPyYkJymzrc22AnugOpHH0iV35ektST3SpkNZHA81H0ELU3NUpyaE1IUAPn8y1HBV7xmnl48oqFsOF770a1GGE/MlZpv21s5126hXFSJhDDlH+GQ7/bW7mNWp3nfkhLNuTFLllpXgocQkqGDHSvFysXJRBKVG3VNvA+B0HO2FlU6pdFtJNGmnnEskbkpcGcD2JhaWPc/8UV/ZEfFOWpWN/GuDtVCvX1X9zKWnWml8f00FIP1jFOspyUSmoXBM90gHKkLPJ/8AcYse5rlSy6mUW1MJJ4Q4keH5RIfg1z8wJ66Z0obSncEEgJhd0pVtpaS+nccsiFi6knKX1fCIxd9UfmqSmWkWvh5BJ2gJH9z3jr6e2GmqyqXpl9xKMcpzxHNS6m4Lg+BkkgSTK8JwOvvDhpLLdMpiGGyEkDmOX4t4i8alV18SfJ57ItsvtfWzfteg02jJDcqyjf5qMJqrs7tYNrAAX8QM4+cONuoMsIW+6rCUIJJzCv0skxcGqb09yptDxXk+YzxDP0ep2X2Wze0kOnGKp47ljJZKkyzQI/IP2iOak1c0Wz6hPhW1zuy22T/kekS9aAlOAPCBCQ7RtTcfmKZbTByt5wLWkdTyAP3j0k5e46KJ12JrZLVJqt2zLCw9Oudy2pXmlPJI+ZJiyQ6RHNN7elrXsym0WWQEJYYTuAJ5URyYkcZSwQQQQAEEEEABEX1Tt9Fz2JV6ORlb0uruiBnCwMg/eJRGCAc5gAqv2YK+tdIqNqzSz8RTHSpAV12kkY+hBh0tqCk5zCFvqWOmnaOl5xpLiafWTuVkeHxnafsrn6w9EEJT4SfUfKH72XWn2PmYUofSNCaWFIwqN15RI5jnPDccekGtodHgrdqu447qW1KOE92E5CVDjrDDtqWQmlNFKPLqIh+v8k7Tbrp9X25bX4Mge8TqwZpicpLfd4OUjPtHI8RxFZVFHHzG5ZTmzcbcWysKXhQ9xER1ntqUuagh6VCU1KXG5A6FSfSJfU2VNPFGOM5EKi+KxNi/mZdhxSEsN4IzwqPOeH13RymoPWhnVCMG5ITwTVKXMKQlTrLiT4sAiNiYmKnUcIXMTDxPGCSQIfb1Mp1SkUPTUoyte3JISMmNGUo1LlRlqVSFZ64jqvx5a5hyKU5yXpZDNP6PN05r41Y2AHKiRE7NaamFhpCgFkdc8R43TNfC2fPlhgpwjqB0iA2nMuuPsKJKsxglB58ZXz41wRcvKS17k9vydZp1kTS8/wBZ4bEHPIzG92YaN3UjNVNweJZABPn6xCdYJvvkUymNn8Q3HHrDx0nk002zJRvaAsoCjiPV/p/HWP4fKfvJjXuU4x9kTN7ahoqUQEgZJ9AIRlh013ULtF/GALXIU13vFKAynagkBPtkwxtTa8aLZc/M7wh1xBaaz/keI2exrbJp9mzdxTLaxM1F8pSVeSUnHHsTGm02pcD7QMAD0EZgghBAQQQQAEEEEABBBBAAhe2RbKqlY0vcUvuS/SXd6ikfkVx9MEgxuaUV5NyWBTKipWXkt908M8hSeOfnjMNq6aQxXbenqTNJ3NTTKm1D59Iq5oDMPW1edw2JPKWkodUprf5qSdvHzHMOg9oI8MdDp5I8o0pg4OR1jceGTnB+UajyRu5+0XNKIZq7QE3FZkyhKMzDA7xpQ65ELTRmrryJJ8lCmyUqBPmIfSme9l3GlfhUCIrJcTM1aWp0wynwNPq3oPkRCbodUHFd+5zc6PaY96mUqSk5HMIvUZJRqQF42pUhOOesNamVP42SaUTnAGSIWWrDZTd8lMkeFbWEx5TDt682TfDaZlue6tol1PIMg0UkYKeI85gBI9VRpW5Md7IBvAJSPONqYC0ncrkDyjlXR6bGgoaaRHdQp5+Vs+ZQlQ2ukIPERWzGlLLCUJO/I6R1tWZlYoku0MBC3ASmNWwylEyhzBOxOQPTiO5iR1hfdsZf6pwR41BKqxqZKyqslLSkpIiylNHw0o0ynACUgYivmlrX8U1Cm59xP4HCBD9ecSywpxatqEJyTnoBHsKq/Kxa6/ps1VRTk5Cs7QFTcqVYo9psEqLrqSoJ5IUo7R+8W2sWit2/aVMpDQIEtLoQonqVADJ+8VK0Okl352g3atM5MtTyXiMZHGQj9RF0fSMdj2x7YQQQRQqEEEEABBBBAAQQQQAB6RVHtG0t+y9Y6TfUolxMtMrR3v8AjuHCsn3B/SLXQtO0han806ZTzTDW+blB8SzjrlPUfURet6ZDPNl1qblGpqXUFNPIC0KHmCI1ZlBB3dYhXZ8r5rWnzcm8vMzTFfDqBOTsH4T+8Tt8A9TzDuzNEHwaqFcdfpCg7R1ALklLV9hsFbCgHPUJ9YcTSU97gxyb1p6Khbc/LKbC9zSsA/KE3tpdUfYVbFSWmJWwqzvlEI3DCgI1dYCk1CmL/MU4ERi0XVMvOy4UQWXCkj0wY7OqrpfZozv/AHYKs+0efnRGvxBOPv8A+HDU24yh8G3biy3tKlHGOREicUXBwM48oiVBdQFIQXCfLmJSnYkDCh7xys+OrGVxZ8C91WWDN0+XzjJyR7RmizrdOp808U8d2QCPWPDU/Yu5pFHOQjJjUqEw21b8yyoeNZASY9Bg0KePXFruaLJ6tiyYaCy+XZqbVkqWoqBid6r1kUmyZt5KyHXcMoHqD1jh6IyQZoCVnAUqOHrO4/Xrwo9nybniecSk4GcKUfSPUZeoelex0KX6d/I5+xVbX8PsaauF4JL1SePdqA57sdMn55iwXpHEsShsW3aVOokulKW5VhKAEjAzjn9Y7ccp8jWEEEEQQEEEEABBBBAAQQQQAEfD7aHWlNOJCkrBBBHBEfcBgAqDZ+/T7X+r2u82WJCorIY54V5ox9yId7yOTx5wqO2hIopNx27dsisNT6V7CegOw7gfc+URWp6/1adk2pajUQCb2ALJ8RJ6ZAHvGhc8hCWkPstlKiVYA9TxGhVqrSJSWcTOVKVZJBHicEV2cRrJeB3JbnmGVnICz3ScRvU/Qq76irvaxWG5fPJ8RcMRLUlpkSbZHlOUiVu2pOOVaWQwt4lCk9FDMet7VW1p+jSaWKl3r7DoJKc4AibSvZ1lBj4yvuuEddrWI6KOzxbePHVJ4+wViDVTkputbRgeBFtycnyLqmztqobDiqylGcfi8okMpVbef/otV6UWfLKokj3Z4t7YQzVp5HH5jmOPUOzonGZC4Sk+i2f+YVdj49r3KtfkXDw2EP8AWTFzqDKrmbuaXJvNzDWwYUhUcevsTLUm224ysbljnETWr6FXpJK309+XmgnoQ5sMRSp0e+7fWk1SmTi0NnO5SCtA+sa8dY9aScWtETxLnJOMk0OXTdgSVvomX1bW22t2fpmOR2eKM5fWuEzcT+1crTHe+8ROQrPgx+sQherE65aszQnqYhDriO7Q82cbfpFkOxTQ0SGmLtVcaKZqoTSy4VJwopScJ+YwYMy9WybRvoi4wSY+E9IzBBGIcEEEEABBBBAAQQQQAEEEEABBBBABVbtw8zNLB5CRkA+XEefZVkpN20pl92Ul3HRMY3qbBVjHrBBDokjmSAAQAAPQRhXSCCBC2fCI+jBBFiGCYzgZgggIPB/8YjWfbbeSpDqEuJI6KGRBBABWLtDykpLXtTBLyrDIUkbg22E55HXEXC0abbbsOQS2hKE7OiRgdBBBCZDSZwQQRUAggggAIIIIAP/Z"
DATA_FILE = "HKED.xlsx"
RESULT_FILE = "sonuclar.json"
PARTICIPANT_NAMES = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.set_page_config(page_title="HKED Turnuva", layout="wide", page_icon="🏆")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');

.stApp {
    background: #f0f2f6;
}

/* Tüm yazılar koyu */
body, p, span, div, label, .stMarkdown, .stText {
    color: #1a1a2e !important;
}

.big-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.2rem;
    text-align: center;
    color: #1a1a2e;
    letter-spacing: 4px;
    text-shadow: none;
    margin-bottom: 0.1rem;
}

.sub {
    text-align: center;
    color: #666688;
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}

.card {
    border-radius: 12px;
    padding: 14px 20px;
    margin: 6px 0 2px 0;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 1. — altın arka plan, KESİNLİKLE siyah yazı */
.c1 {
    background: #FFD700;
    color: #000000 !important;
    font-size: 1.2rem;
    border: none;
    box-shadow: 0 2px 8px rgba(255,215,0,0.3);
}
.c1 * { color: #000000 !important; }

/* 2. — beyaz arka plan, koyu yazı, gümüş border */
.c2 {
    background: #ffffff;
    color: #222222 !important;
    border: 2px solid #aaaaaa;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.c2 * { color: #222222 !important; }

/* 3. — açık turuncu arka plan, koyu yazı */
.c3 {
    background: #fff3e0;
    color: #5c3200 !important;
    border: 2px solid #b87333;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.c3 * { color: #5c3200 !important; }

/* 4-5 — açık gri arka plan, orta koyu yazı */
.cx {
    background: #e8eaf0;
    color: #555577 !important;
    border: 1px solid #ccccdd;
}
.cx * { color: #555577 !important; }

.roast {
    font-style: italic;
    font-size: 0.88rem;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    border-left: 3px solid;
    font-weight: 500;
}

/* 1. roast — sarı arka plan, koyu yazı */
.r1 {
    background: #fffbe6;
    border-color: #e6b800;
    color: #7a5c00 !important;
}
.r1 * { color: #7a5c00 !important; }

/* Diğer roastlar — açık kırmızı arka plan, koyu yazı */
.rx {
    background: #fff0f0;
    border-color: #cc2222;
    color: #aa1111 !important;
}
.rx * { color: #aa1111 !important; }

.prob-row {
    padding: 12px 16px;
    margin: 6px 0;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.prob-name {
    font-weight: 700;
    font-size: 1rem;
}

.prob-yorum {
    font-weight: 700;
    font-size: 0.95rem;
    color: #1a1a2e !important;
}

.prob-bar-bg {
    background: #dde0ea;
    border-radius: 6px;
    height: 12px;
    margin-top: 7px;
}

.section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.6rem;
    color: #1a1a2e;
    letter-spacing: 2px;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
}

/* Metrik kutuları */
div[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #dde0ea;
    padding: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
div[data-testid="metric-container"] label {
    color: #666688 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #1a1a2e !important;
    font-size: 1.8rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #e4e7f0;
    border-right: 1px solid #ccccdd;
}
section[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}

/* Buton */
.stButton > button {
    background: #1a1a2e;
    color: #ffffff;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
}
.stButton > button:hover {
    background: #2e2e4e;
    color: #ffffff;
}

/* Tablo */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* Input alanları */
.stTextInput input {
    background: #1a1a2e !important;
    color: #ffffff !important;
    border: 1px solid #444466 !important;
}

/* Selectbox — seçili değer ve dropdown yazısı siyah */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] span {
    color: #000000 !important;
}
div[data-baseweb="select"] > div {
    background: #ffffff !important;
}

/* Yiğit hover resim */
.yigit-wrapper {
    position: relative;
    display: block;
}
.yigit-hover-img {
    display: none;
    position: absolute;
    top: -160px;
    left: 50%;
    transform: translateX(-50%);
    width: 130px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    z-index: 999;
    pointer-events: none;
}
.yigit-wrapper:hover .yigit-hover-img {
    display: block;
}
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE)
    df.columns = [re.sub(r'[^a-zA-ZçÇğĞıİöÖşŞüÜ0-9]', '', str(c)).upper() for c in df.columns]
    return df

        url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
        headers = {"X-Auth-Token": api_key}
        resp = requests.get(url, headers=headers, timeout=10)
        api_matches = []
        if resp.status_code == 200:
            data = resp.json()
            for m in data.get("matches", []):
                score = m.get("score", {}).get("fullTime", {})
                hs = score.get("home")
                as_ = score.get("away")
                if hs is not None and as_ is not None:
                    api_matches.append({
                        "home": m.get("homeTeam", {}).get("name", ""),
                        "away": m.get("awayTeam", {}).get("name", ""),
                        "homeScore": int(hs),
                        "awayScore": int(as_),
                    })

        # Excel satırlarıyla eşleştir
        fetched = {}
        scores_map = {}
        for idx in range(len(df)):
            row = df.iloc[idx]
            t1 = str(row.iloc[2]).strip()
            t2 = str(row.iloc[4]).strip()
            for m in api_matches:
                if match_team(m["home"], t1) and match_team(m["away"], t2):
                    hs, as_ = m["homeScore"], m["awayScore"]
                    scores_map[str(idx)] = (hs, as_)
                    if hs > as_:
                        fetched[str(idx)] = "1"
                    elif hs == as_:
                        fetched[str(idx)] = "0"
                    else:
                        fetched[str(idx)] = "2"
                    break
        return fetched, scores_map

    except Exception as e:
        return {}, {}

def fetch_todays_matches():
    """ESPN API'dan bugünün Dünya Kupası maçlarını çeker, saatleri TSİ'ye çevirir."""
    import datetime
    try:
        today = datetime.datetime.utcnow()
        date_str = today.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates={date_str}"
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return []
        data = resp.json()
        matches = []
        for event in data.get("events", []):
            comp = (event.get("competitions") or [{}])[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            state = comp.get("status", {}).get("type", {}).get("state", "pre")
            detail = comp.get("status", {}).get("type", {}).get("shortDetail", "")
            date_raw = event.get("date", "")
            try:
                dt_utc = datetime.datetime.strptime(date_raw, "%Y-%m-%dT%H:%MZ")
                dt_tsi = dt_utc + datetime.timedelta(hours=3)
                time_str = dt_tsi.strftime("%H:%M")
            except:
                time_str = "?"
            matches.append({
                "home": home.get("team", {}).get("displayName", "?"),
                "away": away.get("team", {}).get("displayName", "?"),
                "time": time_str,
                "state": state,
                "detail": detail,
                "home_score": home.get("score", ""),
                "away_score": away.get("score", ""),
            })
        return matches
    except:
        return []

def load_results():
    # Önce GitHub raw'dan oku (deploy'dan etkilenmez)
    try:
        url = "https://raw.githubusercontent.com/cenkcatalbas-lang/HerkonununEndogrusu/main/sonuclar.json"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    # GitHub'dan gelmezse local dosyaya bak
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

DEFAULT_ROASTS = {
    1: [
        "TANRI MISALI HÜKÜM SÜRÜYOR 👑 Diğerleri senin gölgeni bile göremez.",
        "Rakipler bu ismi duymaktan titremeye başladı. Haklılar.",
        "Tahmin makinesi. Diğerleri ne yapıyor ki zaten?"
    ],
    2: [
        "İkinci olmak; birinci OLAMAMAKtır. Ama ne yaparsın, bu senin tavanın.",
        "Zirveden bir adım uzakta... ya da onu hiç göremeyecek kadar mı?",
        "Gümüş madalya: altın olmak için YETERSİZ olduğunun kanıtı."
    ],
    3: [
        "Üçüncü olmak yarı-başarısız olmaktır. Tebrikler sanırım? 🥉",
        "Podiyuma zar zor tutunuyor. Aşağı bakma, görünce üzülürsün.",
        "Bronz. Gurur duymak için sebebin yok, ama alışmışsındır zaten."
    ],
    4: [
        "4. sıra. Resmen orta halli başarısızlık. Ne ön ne son, sadece VAR.",
        "Veriye bakılırsa maçları tahmin etmek yerine uyumuş.",
        "Kim olduğunu hatırlatmaya gerek yok, çünkü kimse hatırlamıyor zaten."
    ],
    5: [
        "SONUNCU. 💀 Bu sonucu kelimelerle anlatmak bile acı verici.",
        "Turnuvada varlığından kimse haberdar değildi, skor da bunu kanıtlıyor.",
        "Tebrikler! En değersiz tahminler ödülünü kazandın. Kupa yok tabii. 🗑️"
    ]
}

ROAST_FILE = "roasts.json"

def load_roast_settings():
    try:
        url = "https://raw.githubusercontent.com/cenkcatalbas-lang/HerkonununEndogrusu/main/roasts.json"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    if os.path.exists(ROAST_FILE):
        try:
            with open(ROAST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "enabled": True,
        "custom": {},
        "rank_roasts": {str(k): v for k, v in DEFAULT_ROASTS.items()}
    }

def save_roast_settings(settings):
    with open(ROAST_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def get_roast(name, rank, total, settings):
    if not settings.get("enabled", True):
        return None
    if name in settings.get("custom", {}):
        return settings["custom"][name]
    key = str(rank) if rank <= 3 else ("5" if rank == total else "4")
    roasts = settings.get("rank_roasts", {}).get(key, DEFAULT_ROASTS.get(int(key), [""]))
    return random.choice(roasts) if roasts else ""

def win_probability(scores, df, results, participant_names):
    total_matches = len(df)
    played = sum(1 for v in results.values() if v != "Oynanmadı")
    remaining = total_matches - played
    ratio = remaining / total_matches if total_matches > 0 else 0

    total_score = sum(scores.values())
    if total_score == 0:
        base = {p: 1/len(participant_names) for p in participant_names}
    else:
        base = {p: scores[p]/total_score for p in participant_names}

    uniform = {p: 1/len(participant_names) for p in participant_names}
    alpha = 1 - ratio
    final = {p: alpha * base[p] + (1 - alpha) * uniform[p] for p in participant_names}
    s = sum(final.values())
    return {p: v/s for p, v in final.items()}, remaining

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Admin Paneli")
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Yanlış şifre!")
    else:
        if st.button("Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()

        st.write("---")
        df_temp = load_data()
        results_admin = load_results()

        for idx, row in df_temp.iterrows():
            m_label = f"{row.get('TAKIM1','T1')} - {row.get('TAKIM2','T2')}"
            results_admin[str(idx)] = st.selectbox(
                m_label, ["Oynanmadı","1","0","2"],
                index=["Oynanmadı","1","0","2"].index(results_admin.get(str(idx),"Oynanmadı")),
                key=f"match_{idx}"
            )

        if st.button("💾 Kaydet"):
            try:
                with open(RESULT_FILE, "w") as f:
                    json.dump(results_admin, f)
            except:
                pass
            st.cache_data.clear()
            st.success("Kaydedildi!")
            st.rerun()

        st.write("---")
        st.markdown("### 🎭 Espri Yönetimi")

        rs = load_roast_settings()

        # Esprileri aç/kapat
        enabled = st.toggle("Esprileri Göster", value=rs.get("enabled", True))

        st.markdown("**Kişiye Özel Espriler**")
        custom = rs.get("custom", {})
        for p in PARTICIPANT_NAMES:
            if p == "YİĞİT":
                st.caption(f"YİĞİT — sabit espri (değiştirilemez 😂)")
                continue
            val = custom.get(p, "")
            new_val = st.text_input(f"{p}", value=val, key=f"roast_custom_{p}",
                                     placeholder="Boş bırakırsan sıra bazlı espri gelir")
            custom[p] = new_val if new_val.strip() else ""

        st.markdown("**Sıra Bazlı Espriler**")
        rank_labels = {"1": "👑 1. sıra", "2": "🥈 2. sıra", "3": "🥉 3. sıra",
                       "4": "😐 Ortalar", "5": "💀 Sonuncu"}
        rank_roasts = rs.get("rank_roasts", {str(k): v for k, v in DEFAULT_ROASTS.items()})

        for key, label in rank_labels.items():
            with st.expander(label):
                roast_list = rank_roasts.get(key, [])
                new_list = []
                for i, r in enumerate(roast_list):
                    edited = st.text_area(f"Espri {i+1}", value=r, key=f"roast_{key}_{i}", height=70)
                    new_list.append(edited)
                # Yeni espri ekle
                new_roast = st.text_input("+ Yeni espri ekle", key=f"roast_new_{key}")
                if new_roast.strip():
                    new_list.append(new_roast.strip())
                rank_roasts[key] = [r for r in new_list if r.strip()]

        if st.button("🎭 Esprileri Kaydet"):
            new_settings = {
                "enabled": enabled,
                "custom": {k: v for k, v in custom.items() if v},
                "rank_roasts": rank_roasts
            }
            save_roast_settings(new_settings)
            st.success("Espriler kaydedildi! GitHub'a da yükle: roasts.json")
            st.rerun()

# --- ANA BÖLÜM ---
st.markdown('<div class="big-title">🏆 HKED TAHMİN TURNUVASI 🏆</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">KİM KAZANIR? KİM EZİLİR? HERKES YARGILANIR.</div>', unsafe_allow_html=True)

try:
    df = load_data()
    roast_settings = load_roast_settings()

    results = load_results()

    scores = {p: 0.0 for p in PARTICIPANT_NAMES}
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            idx = int(idx_str)
            if idx < len(df):
                row = df.iloc[idx]
                try:
                    odd = float(row[res])
                    for p in PARTICIPANT_NAMES:
                        if str(row[p]) == res:
                            scores[p] += odd
                except:
                    continue

    played = sum(1 for v in results.values() if v != "Oynanmadı")
    remaining = len(df) - played

    # Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("⚽ Toplam Maç", len(df))
    m2.metric("✅ Oynanan", played)
    m3.metric("⏳ Kalan", remaining)

    col_refresh = st.columns([3,1])[1]
    with col_refresh:


    st.markdown("---")

    sorted_p = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_p = len(sorted_p)

    rank_icons = {1:"👑", 2:"🥈", 3:"🥉"}
    fire_icons = {1:"🔥🔥🔥", 2:"🔥🔥", 3:"🔥"}
    card_cls   = {1:"c1", 2:"c2", 3:"c3"}

    st.markdown('<div class="section-title">🔥 ATEŞ SIRALAMASI</div>', unsafe_allow_html=True)

    for rank, (name, score) in enumerate(sorted_p, 1):
        icon = rank_icons.get(rank, "💩" if rank == total_p else "😐")
        fire = fire_icons.get(rank, "🧊" if rank == total_p else "💧")
        cls  = card_cls.get(rank, "cx")
        roast = get_roast(name, rank, total_p, roast_settings)
        if name == "YİĞİT":
            roast = "Buralar sana fazla aslanım, yallah 9gag'e 😂"
        rcls = "r1" if rank == 1 else "rx"

        if name == "YİĞİT":
            roast_html = f'<div class="roast {rcls}">💬 {roast}</div>' if roast else ""
            st.markdown(f"""
            <div class="yigit-wrapper">
                <img class="yigit-hover-img" src="{YIGIT_IMG}" alt="yigit">
                <div class="card {cls}">
                    <span>{fire} #{rank} {icon} {name}</span>
                    <span>{score:.2f} puan</span>
                </div>
            </div>
            {roast_html}
            """, unsafe_allow_html=True)
        else:
            roast_html = f'<div class="roast {rcls}">💬 {roast}</div>' if roast else ""
            st.markdown(f"""
            <div class="card {cls}">
                <span>{fire} #{rank} {icon} {name}</span>
                <span>{score:.2f} puan</span>
            </div>
            {roast_html}
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">📊 PUAN TABLOSU</div>', unsafe_allow_html=True)
    chart_df = pd.DataFrame(
        {"Puan": [scores[x[0]] for x in sorted_p]},
        index=[x[0] for x in sorted_p]
    )
    st.bar_chart(chart_df, height=280)

    st.markdown("---")

    st.markdown('<div class="section-title">🎯 TURNUVA SONU KAZANMA OLASILIKLARI</div>', unsafe_allow_html=True)
    st.caption("Kalan maç belirsizliği hesaba katılarak ağırlıklı olasılık yöntemiyle hesaplanmıştır.")

    probs, n_rem = win_probability(scores, df, results, PARTICIPANT_NAMES)
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    prob_colors = {1:"#e6b800", 2:"#888888", 3:"#b87333"}

    for rank, (name, prob) in enumerate(sorted_probs, 1):
        pct = prob * 100
        if pct > 50:   yorum = "ÖLÜMSÜZ 👑"
        elif pct > 30: yorum = "KUVVETLİ ADAY 🔥"
        elif pct > 15: yorum = "ŞANSI VAR 🍀"
        elif pct > 5:  yorum = "ZORLANACAK 😬"
        else:          yorum = "UMUT YOK 💀"

        color = prob_colors.get(rank, "#555577")
        text_color = "#000000" if rank == 1 else "#ffffff"

        st.markdown(f"""
        <div class="prob-row" style="border-left: 4px solid {color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="prob-name" style="color:{color};">#{rank} {name}</span>
                <span class="prob-yorum">{pct:.1f}% — {yorum}</span>
            </div>
            <div class="prob-bar-bg">
                <div style="background:{color}; width:{min(pct,100):.0f}%; height:12px; border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">⚽ MAÇ SONUÇLARI</div>', unsafe_allow_html=True)

    match_cards = []
    for idx_str, res in results.items():
        if res != "Oynanmadı" and idx_str.isdigit():
            row = df.iloc[int(idx_str)]
            t1 = str(row.iloc[2]).strip()
            t2 = str(row.iloc[4]).strip()
            try:
                hs = float(str(row.iloc[5]).replace(",","."))  # 1.00 kolonu
                ds = float(str(row.iloc[6]).replace(",","."))  # 0.00 kolonu
                as_ = float(str(row.iloc[7]).replace(",",".")) # 2.00 kolonu
            except:
                hs, ds, as_ = None, None, None
            match_cards.append((idx_str, t1, t2, res, hs, ds, as_))

    if match_cards:
        # 2 kolonlu grid
        for i in range(0, len(match_cards), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(match_cards):
                    idx_str, t1, t2, res, hs, ds, as_ = match_cards[i + j]
                    # Skoru reverse-engineer et: oranlardan değil sembolik yaz
                    real_score = None
                    if res == "1":
                        score_display = f"{real_score[0]} - {real_score[1]}" if real_score else "✓ - ✗"
                        color = "#22c55e"
                        label = f"🏆 {t1} kazandı"
                    elif res == "0":
                        score_display = f"{real_score[0]} - {real_score[1]}" if real_score else "— —"
                        color = "#f59e0b"
                        label = "🤝 Beraberlik"
                    else:
                        score_display = f"{real_score[0]} - {real_score[1]}" if real_score else "✗ - ✓"
                        color = "#22c55e"
                        label = f"🏆 {t2} kazandı"

                    t1_bold = f"<b>{t1}</b>" if res == "1" else t1
                    t2_bold = f"<b>{t2}</b>" if res == "2" else t2

                    col.markdown(f"""
                    <div style="background:#ffffff; border-radius:12px; padding:14px 16px;
                                margin:4px 0; box-shadow:0 1px 4px rgba(0,0,0,0.08);
                                border-top: 3px solid {color};">
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                            <span style="color:#1a1a2e; font-weight:600; font-size:0.9rem; flex:1; text-align:right;">{t1_bold}</span>
                            <span style="background:{color}; color:white; font-weight:800;
                                         font-size:1rem; padding:4px 12px; border-radius:8px;
                                         white-space:nowrap;">{score_display}</span>
                            <span style="color:#1a1a2e; font-weight:600; font-size:0.9rem; flex:1; text-align:left;">{t2_bold}</span>
                        </div>
                        <div style="text-align:center; margin-top:6px; font-size:0.78rem; color:#666;">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Henüz sonuç girilmemiş.")

    # --- BUGÜNÜN MAÇLARI ---
    st.markdown('<div class="section-title">📅 BUGÜNÜN MAÇLARI</div>', unsafe_allow_html=True)

    import time as _time
    now_ts = _time.time()
    if ("today_matches" not in st.session_state or
            now_ts - st.session_state.get("today_fetch_ts", 0) > 180):
        st.session_state.today_matches = fetch_todays_matches()
        st.session_state.today_fetch_ts = now_ts

    today_matches = st.session_state.get("today_matches", [])

    if today_matches:
        for m in today_matches:
            state = m["state"]
            if state == "post":
                badge = f'<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">BİTTİ</span>'
                score_str = f'<b>{m["home_score"]} - {m["away_score"]}</b>'
                time_color = "#22c55e"
            elif state == "in":
                badge = f'<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;animation:pulse 1s infinite;">🔴 CANLI {m["detail"]}</span>'
                score_str = f'<b>{m["home_score"]} - {m["away_score"]}</b>'
                time_color = "#ef4444"
            else:
                badge = f'<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:700;">BEKL.</span>'
                score_str = "vs"
                time_color = "#6366f1"

            st.markdown(f"""
            <div style="background:#ffffff; border-radius:12px; padding:12px 18px; margin:6px 0;
                        box-shadow:0 1px 4px rgba(0,0,0,0.08); display:flex;
                        align-items:center; justify-content:space-between; gap:12px;">
                <span style="color:{time_color}; font-weight:800; font-size:1rem; min-width:52px;">
                    TSİ {m["time"]}
                </span>
                <span style="color:#1a1a2e; font-weight:600; flex:1; text-align:right;">{m["home"]}</span>
                <span style="color:#1a1a2e; font-weight:800; font-size:1.1rem; min-width:60px; text-align:center;">{score_str}</span>
                <span style="color:#1a1a2e; font-weight:600; flex:1; text-align:left;">{m["away"]}</span>
                {badge}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Bugün maç bulunamadı veya API erişimi yok.")

    st.markdown("---")
    st.markdown('<div class="section-title">📋 TÜM FİKSTÜR</div>', unsafe_allow_html=True)
    with st.expander("Fikstürü Görüntüle"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Hata: {e}")
    st.exception(e)
