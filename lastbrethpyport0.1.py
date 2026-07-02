#!/usr/bin/env python3
# last breath 4k 0.2 — files = off • python 3.14 • locked 60 fps • all assets in RAM
# 0.2: main menu, font cache, rotation cache, threaded OST prebuild, scaled window

from __future__ import annotations

import array
import base64
import io
import math
import random
import struct
import sys
import threading
from typing import List

import pygame

FILES_OFF = True
MUTE = False
FPS = 60
WIDTH, HEIGHT = 640, 480

# Last Breath Phase 1 HUD layout — procedural, files = off
LB_BOX = pygame.Rect(170, 238, 300, 162)
DLG_BOX = pygame.Rect(32, 368, 576, 96)
STATS_Y = 432
SANS_X, SANS_Y = 320, 108
MENU_OPTS = ("FIGHT", "ACT", "ITEM", "MERCY")
PHASE1_TURNS_TO_CLEAR = 5

# base64 PNG — real Undertale wiki Sans sprites (files = off, RAM embed only)
SANS_ANIMS_B64 = {
    "idle_0": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAADuUlEQVR42u3d0Y6jMBBE0WQ1///L2afRSmgRAXfbbfvU42gIDs2luowD79fr9XnRcvrjECgsTaSfGQf9+eS6x/v9RizV1Lty85RN5sokIxax+xE6M8GIRSxSZyIXsYhF6kzkIhaxSJ2JXMQuKoVVWOKxm3prJa9FrEsxKSwNV8kVFHe9qdW7e+8PsTQ3sa3d4+/2d0l6ut/jdhUJRixi18p5Gd+jErmIRew4HUnIJr33/hBLCquwtKRKrKBo9bCzbvTbvBm9fysoaO2ueLYu1Fwx7eWxrWf+1UzPFfFX27WOC7G0tsfeJSHL434/d4a7N4jlsXW8NdvrsrxdjqW9PfYpub2eKlPZexGL2H5db5Uu9corK5OLWMT265LvEpw9rhlzLWIR26+rvCLzjPBv//7tdk/zN2Jpzxx7JLd3F9q6v6wVG4hFbG6Xe3amfktErxUWT7vfu9v16O4Ru6hC7+48PcNb82HUmd/6a71KXTNiEZt/xkcRnN0lt+ZbHktjib07U9TqQdXe4tG6WjKDXMQidlzerarW8Wfmc8Qitv6Zn/X/2Tk1g1zEIrZfV3eX4OwZq1ZSvz1OkccTsYit72nZc9VPx99rO8RuoJ/eZ1KEF/6Oo3WFRfU1TC3HG7E7EzuK1Kde+e04j4RXWdl/HMeT449YHltfVTwziviWKwhidyS2irdGEXDlpa37yfbmO/VALI/NJ+Zujs3uRp8SWqG7RuxOxFbyiv/9/1n+jM7DdwntlWsRi9g+GrViv/XzWq8MI9IFYhE7/kzNmtPN6rpHdseI3YnYiLsLlT16ByF2R4+tSm52Vxydk0d8X8Tu3BWPJjd7pUPVZyK2/EIAsXLsObmrda2jvTXiuCIWsfU9KYqwUXPakVdAxCL2ObnZb5+stlbp7vHI6FEQu6hSftEe/ZSYKp8b5dk90gRiETvew2Z9msyIcSMWsTSTECvH7qenXlnhPi5iERtHwIhcx2MJsa2kLhs1CqyZQixi63SdrhSIReyK+bPa+mDEksL2vhLM8LZnheWxNFueRSxi43Jk77nhHbtjxCJ2nvxKiEXsjN1otDcjlhSWFJYUlhRWVyxfHr9PryefI5b+RbVX4Tc+Z+XX7HcKIJbWJpYQSwrb5vmzd/IKK8fGdbl381+VZxo+7YpHvK8HsbrivHx4dd+z+ntfo2agPJmN+nhs1LMMZ1uxED3eyFWUiEVsfxKq77fylQWxiO3XlZ55VxbJUXm10pUKsXIszSTEKiwpLCksKSwpLCnsovoLa3qPSNZjLI0AAAAASUVORK5CYII=",
    "idle_1": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAAD0klEQVR42u2d2w6jMAxEy4r//+XuU7USWgSJLxk7Zx6rUgjOydhJCsfn8/l+UDv94Rb01Fnxor/f2EHmOA6IRZo6lD02mszOJEMsxO5HaGWCIRZiIbUSuRALsZBaiVyIhVhIrUQuxDYVgSWwCI/d1FuVvBZiGYoRgUXLJbmDYtSbrN6dfT6IRbWJtWaPv+NHSZo97/U4RYIhFmJ71XkR7VAiF2Ihdp2uJESTnn0+iEUElsCilpLYQWH1sLts9G296X1+dlCg3llxtSyUuWK0l8dae/7TTM8T8U/HWa8LYlFvjx0lIcrjfr9bYfUGYvFYHW+N9roob6eORXt77Cy5WU+VUfZeiIXYvKxXJUt98kplciEWYvOy5FGCo6+rYl0LsRCbl1U+kXlH+NvP3x43W39DLNqzjr2Sm52FVqhXSwa2uqK24sgH9i0RWTssZrNfxR0fZ7eeqkxqZtkWsrrjvbMhixivf+spkH5266nKpGa2Wyp5mvU4lbnj7bPibuSOkprR/hLrsdmEduhwZwaBT1OHXbPmu/Zcy7yIdp+dbhgKLnd2qXet1x85YrEIALH6PT/q+9F1agS5EAuxefXoKMHRU5FWUt/eJ8/7CbEQq+9p1sl3bw+1tttCLsQ21Zndkzy88Hcd1q0z6pvTLPcbYncmVnU15mku9u3x1/at3rx2vY6Z+w+xeKy+VDzTi3jLCAKxOxKr4q1eBDx5qfU80d48Eg+IxWPjiRmtY6Oz0VlCFbJriN2JWCWv+N/3vfcMWVd5onOQmREAYvFYv56nkiW//T3ryLCiuoBYiF3fU6PmdKOy7pXZMcTuRKzH6oKyR+8giN3RY1XJjc6KM/5bE91eiN05K15NbvROB9XH/lj+IQCx1LH35HbLWld7q8d9hViI1fckL8JWzWl7joAQC7Hz5Ea/VlRtr9Lo/YjIUSC2qVIfuWftoat/18uzM6oJiIXY9R5W9WkyK64bYiEWVRLEUsfup1mvVFjHhViI9SNgRV2HxyKItZLattQQ2DMFsRCrk3UyUkAsxHasP9X2B0MsIrDZI0GVV44SWDwWVapnIRZi/erI7LnhHbNjiIXYOvUrgliIrZiNenszxCICiwgsIrCIwJIVU19e25P15HOIRf9KtY/wG5+j6tfodwpALOpNLIJYRGBtnl89kyew1LF+We5o/afyTMPZrHjF+3oglqw4rj58WvdUf++r1wwUT2ZDOR7r9SzDajsWvK/XcxclxEJsPgnq51UeWSAWYvOy0jvviiLZq15VGqkgljoWVRLEElhEYBGBRQQWEVhEYJvqL3GWmWJfNC9nAAAAAElFTkSuQmCC",
    "clenched": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACMAQMAAACOMjPzAAAABlBMVEUAAAD///+l2Z/dAAABjElEQVRIx7XWsWolMQyF4R/UGvQqhm0H9OqCaQP3VQxuBWeLyWaTnRlPIOwpv8IuZIsDALg0+Jx/wSQpVxCSVCuQJGkBdkDegx8wfgJxQP0IBhK+AoiCBWwHbCsYUf4zcKiAsYBBBb4A0xz++jKXE/jwsQKfGq7XWMCQpH0F5lKxgtnBfAFWsdWMXIB8q6F9EOMMXnhqbLXLC9UZQsQIQVSkSWeQ0ur4QGpcA13p0qDM/ApGpg0AG7arzhDakyIbkYxrcPBUIXKjnaGzkVYxIo1+DY0091kYnX6GRiOtwRtGLiDyDQfyDAakVcwi7mGqxXyzCcYZSCj2mC0M2hV0SF4xKy3pV9AwmDFbUpZXYBmwx2zJq7gCYsIr5oT3V3cCDH7F/PUI2wNgHbuHQUgDv4c6Vpu4A973s9/DN2PZ7qGPJ8gD7B72xB6h5TdgPMPHGE5gDq0/wfYIvfO/QdA7FbcAUvqXJnCC76UtwIcAV9YdhAII+Z+LTyC9gKiPKnAB+V467mEmaOrvoZ/gN90MbCk6zT9iAAAAAElFTkSuQmCC",
    "fatal": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSAQMAAACaML3nAAAABlBMVEUAAAD///+l2Z/dAAABc0lEQVRIx+3UMYokMQyF4R+UGnQVH6BAV9ujCTotqKsIKjW8Cbp7mBnbE2y0wSr7AhsjSw/+179SIeWWLklbSpJqQ5MkjQ1d+nrXD8aT+Td86vMdP1mmwZagwjccoMI2LFDBlqnqe/529sBqYLlmpNUgNnRdGfGlz985IuOxY0gZ0pUrxqvtV62owyQNu1gyTsDi7AuaXTXu+1RvC4KP474fwpc05X37Z3u+sYEGqIwF+3u8G31mWj5Xo3FMtNcUdBq+ouOyzoFNbJgluoqB5YJXEVf3c8EDK8fOPhqsiEEUvmTDCjq2oNMwB1/SsmFHYmXYRKrBOeAwnInR4FRhD46Z3uCkgaiZ5omk7B7MJAqladhY0d75cizoz0128DEzBhzQPEMzMx7l0KLEn5l+D4MW91jRJItqoVoRybo3Vy4Zw7HLlcbETowG9yXWvAuwDZ+hZ6LNbO9I3DFf+dhn2q8k/Z2tuWA/Xj9mLPjOaR8r/lIfZF/vYj3YLbUAAAAASUVORK5CYII=",
    "glow_0": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAD3UlEQVR42u2dSZbbMAwFrTytc+Isc+K+gLNyFnqt5oQPAlD9ZbdlcUARg2jqeL1e7xdKo18MQS6dWRr6fmsXguM4IAwJDCuaD1OTlJ08CIOw3ERFJw7CIKwmWVFIgzAIq03WbtIgDMKeQdYu0iAsmZgwJgyl9mHVfZe3L4MwlkTEhKH/CvPEeXTtX/WN3veDMAjLFU19rh+1/Lv7/n1/ffv3P8fvb6/bRRyEkYf9vPZb5ymrhN2RdUead/8gDMJyEtbyWa3/QxiCMHwYqk+YyhLvyOrNl3pJi0IWhEHYmq+xqu3NEubdfgiDsD2ktSx4lpjWdavt8hKEJVPYX2B6Vcc/3xulGg9h+DBtlKjyJSrfSZSIcvmwWdK8ThnY7dsgDMLWfM7uqK3li3aTBmEQNudzRolTtytqXgZhEDa39rdIuiOy9++9183mjxCGcuRhV9K8o7Io+VaaCcsuqwemYSas14K99kzMRoO7TsI5s1hWVrKs0xOzar31k2AvC7f69YsXmWcWy8pKlnW/twcdsz4kSm2xbJRYjbRRsqz6H/Z5mDdRWQzpVBHTKkFVjSLv+nNNZ2b7fWYfiKcpzEbSLBOy2v7VFYbiL4T5Wqrq8+o8a5Y0CKtOmCqfGiVOXdJaJat3nEbHE8KqEhbVZ6wWXVU/NFRdB2HJdKosxjpR/rRjdQtBtE01o+MNYVUIi1pdb9Xqeq+/9m/3pptrO+7GH8Kq+bDoiuKTrAhtEQ9h2QmL4rusLLblq1bvo/Z91/ZDGD5szMKtKxrWPqOXKK9oE8KyEua9Fo9+3mpPxGj0uOsJ+R2xEIYP01ii9Qqg3rGsirYh7OmEWVuWquanikLV0SKEZSWst1rsLTaQQlgtHxaVNHWUaJ3nqfoLYVWixN2kqZ8MRz3eobUjGMKq5WF3pFWL4nb7rt5xhbCqlY6oa74VEbtqnqMrFoRVJWyUNPXrp6LtxRgdj9lxgbBkkh9dtGpRu7/XyidarTgQ9lTCVBac9XQBVbshDMKQUhDGhKFQiXN1zQYPXsVjCIOwPsurfgwfhCEtYdUPZ75L8NX9hjAI00RhkA1hEBYhf4q2IRTCCOtRi9xIG4+YMHzYs6X2oRD2dMKi1A6rRosQhg/bk38R1iMI8/BZ1r4PwhATxoQhJgwxYUSJ5Eft/ngdbQthVdKXV7BXKqryL/UhzxCGYhGGIIwJe5Ki7d1gwsjDxqKw0fwlyiFds1Gi6gUFEPa0KHH1Bdi7XpVh1X7r74EwfJhN5SDaS0OtVobVcYAwCNNabvT77l4JIAzCbH2ZijyrfMubcAh7Wh6G8GHoB/0D4aHHSp2uhSsAAAAASUVORK5CYII=",
    "glow_1": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAD2ElEQVR42u2dS5bbMAwE7TwdLEfPzZyVs9ALhz80CEDVy8QaUySLDUA09X69Xp8XSqNfdEEuXVka+vloF4L3+w1hSDCxonmYmqTs5EEYhOUmKjpxEAZhNcmKQhqEQVhtsk6TBmEQ9gyyTpEGYcnEgDFgKLWHVfcuby+DMJZExIChfwrzxHl27d/1Ru/vgzAIyxVNfa+fnfmt7/18fjc+/+e/150iDsLIw35e+63zlF3CWmS1SPO+PwiDsJyE9Tyr9/8QhiAMD0P1CVPNxBZZo/nSKGlRyIIwCNvzGqva3iph3u2HMAg7Q1o/f1ojpnfdbru8BGHJFPYXmF7V8e/fjVKNhzA8TBslqrxE5Z1EiSiXh62S5nXKwGlvgzAI2/Oc01Fbz4tOkwZhELbmObPEqdsVNS+DMAhbW/t7JLWIHP330etW80cIQznysDtp3lFZlHwrzYBll9UD0zADNjqDvfZMrEaDp07CubLMrKxkWacnZtV66yfBXjPc7tcvPmReWWZWVrKs7/t40LHqIVFqi2WjxGqkzZJldf9hn4d5E5VlIl0qYnolqKpRZOt+7unM6n1f2TviaQqzkTTLgOy2f3eFofgLYb4zVfV5dZ61ShqEVSdMlU/NEqcuae2SNdpPs/0JYVUJi+oZu0VX1Q8NVddBWDJdqhljnSh/27G7hSDapprZ/oawKoRFra73anWj19/v7/Smm3s7Wv0PYdU8LLqieJIVoT3iISw7YVG8y2rG9rxq93vU3ndvP4ThYXMz3LqiYe0Zo0R5RZsQlpUw77V49vNWeyJmo8dTT8hbxEIYHqaZidYrgHrHsirahrCnE2Y9s1Q1P1UUqo4WISwrYaPVYm+xgRTCanlYVNLUUaJ1nqe6XwirEiWeJk39ZDjq8Q69HcEQVi0Pa5FWLYo77V2j/QphVSsdUdd8KyJO1TxnVywIq0rYLGnq109F24sx2x+r/QJhySQ/umh3Rp3+u1aeaLXiQNhTCVPN4KynC6jaDWEQhpSCMAYMhUqcq2s1ePAqHkMYhI3NvOrH8EEY0hJW/XDmVoKvvm8IgzBNFAbZEAZhEfKnaBtCIYywHvXIjbTxiAHDw54ttYdC2NMJi1I7rBotQhgedib/IqxHEObhWdbeB2GIAWPAEAOGGDCiRPKj/v14HW0LYVXSl1ewVyqq8i/1Ic8QhmIRhiCMAXuSou3dYMDIw+aisNn8JcohXatRouoFBRD2tChx9wXYp16VYdV+678DYXiYTeUg2ktDrVaG3X6AMAjTztzo33t6JYAwCLP1MhV5VvmWN+EQ9rQ8DOFh6Af9BbvRx0rwoYivAAAAAElFTkSuQmCC",
    "shrug": "iVBORw0KGgoAAAANSUhEUgAAAHgAAACmCAYAAAARUEuNAAAETklEQVR42u3d0a7jKgyF4fRo3v+V99yckWYqRQlgg0m+dd2SpuTHy8TA5ziOn4Meq//8BTqYdDDpYNLBpINJB9Pf+rX6B/z8/JuGfz4fvYJgKkvwXWK/P3cmxCP41focyXPR0cQiGcE0Iwb/IfKKrFFyW0eQtxGPYATHEJNmIv4nsfW6b8m/EYzgmq62tf1v0nvJRzA9k+C7rrk3hn63e/fzTycUwQiu4ZpH82XEIhjBFXU1E9VK7PdIEdUOgmlvgqOf6KzYHtXuLnPcCEbwGvXOPGUR20v2aqIRjOA1rvnuk7+a2Oj7QTA9Kw/ejdhqJCMYwbl5aqub3l2zSUYwgttiYnZeSQimyi76Le91Z8ViBBuiSQeTGBztmltj1+zVi1U8BIIRXMtdz3bnvdetMmeOYATvTe7b83sEI/ieW1xN2uxaqF3WFyP44dLBOpi2NnfH4D5ZUTH4qv45qv3efDX6+io66B158G6u9WokEIOpVgyeHYtv39jF93t3FIj6XQimd8XgVjKyYuDZSFW1hgzBYvDaWNwbY0djYVbslweTGBxBcnbMrFLfjWAEjz25UbHm6qyHVa726v5Wk4xgBNdQ6+kts1xq9bwYwfLgtXlx1L5YV++ZR79XLf9FsBhci+S77c52raPXy97zEsEIXvOEt8a2WRUfvW659XtRIx6Cuei5eewoydnudXR14myXjWAEr3XTV+RXq6ToPR/57L7EYNqb4N4YPut9b3a+O0oyghFci+TZeW+W647yIAh+uR5TF301IvS69+j9sUZPZ239XQgWg/eKxdH5cm+szHLLCKaaBI+64WiSo2aksmP91fcQzEUnDyFBFRFnpI5WfFSrsWolGcEI3txknDzZrWcjRr2Xzhr5zkhGMIKfpSoxNfqE87P2EIzgZ5DZ60q/2x29Tnbs/v79CEbw2rwuq+54Vt6etd/WXSEYwTVIbv189E4Do2+Vst352YiAYATP1aoVCKPtRb3XtrKB9iI4+snNmjPOcunZbhrBCN5LTzkpDcH0ToJnueisHf2i7xfBCN4r9ma76Grrka+qUhGMYJqRv0eTi2AEP1PZ+1dnu/3WlSAIRnCtmNLbXrVaqtad+3r/FwQjeA6xs13q6Mr9aKLvnv3QKgQ/3VQei9cHRxOxy9ukWbsEIRjBtLMQzEVTRiydNZeNYASvIeKqilHtFYLpKDgX/RYyZ9V0IRjBe7pUIweCEfyG/LVafTOCSQevHhkq1U7rYDGYds6HEYzguW52Vv47myQxmMTgyBFDmkQIfoJ7jY7dCCYdTDqYdDDpYC5afjp6P7N2okfwW9PBY5O1SbNXH2af+YBgehfBhGDSwbGeYAfnr4PlwWtccWv+WGXPyF4XnXXeEoK56Br57NV71+rn/kbNaNnpjtbE4Ki9IqtXULSOPKP/A4IRvKl5WOSaR/e4lAfTuwm+isVZZEflu7NHEATLg2lnIfjh+g3JhfWKQ2i07gAAAABJRU5ErkJggg==",
    "point": "iVBORw0KGgoAAAANSUhEUgAAAHgAAACmCAYAAAARUEuNAAAER0lEQVR42u3d0c7bIAyG4XTa/d/yv6NJW6UoAYwxyfOdbWqTv3Vf/BkM+RzH8XPQY/XLVyDAJMAkwCTAJMAkwCTAAkwCTAJM6/U7+4Y/P/9PfX8+H1FAMJUl+C6x3687E+IRTP8CcUxaD/5L5CixSEYwZebgKzJHye29/1uJRzCCa+XIv9dtHQneWn8jGMExrjl7RPgmvZd8BNM7c/BoDv0m9u7rR3Pz0+pwBCN4jcueRezb6m0EI3hODuslo/V+30Sd/Tvqc1SrtxGM4BxXGUVQq/vOytWrSEYwgtfUx631cvUZqlUkIxjBtbT7nHI2yQhG8BpCq7ri3YRgBM+tW69y01OJzcrFCEZwW86M/oUTgulJdXDvyJG9k6LKCIRgBOcSOatTImo9ufd9q4hGMIL3yrXVP0c2yQhG8B7K7oXaZa8Tgh8uARZg2trcHZ1ndMzOQdHXv1tfz6rDV+VsBHPROXVd66k81etjc9FUOwffJW/0eqP7d3tzavQeqVUjD4Ll4DZSVuXGrNWb3XrHEIzgNSS27knKJqg3R9vZQDUJXpWLs0/XWTVPgGDaIwe31o+rXe3VSLWaZAQjuEYubn32Q5YHqF4XIxjBNevh3tWnu/9/932t7txcNO1BcFZd/H39bNc6er/ZZ14iGMFrSG5dF87q+Oh1y63vixr5EPxwTXvyWdQvMrrDI7oejyY3euRBMILXknyVW6t1UkTVx3IwPYPgXpectd47u94dJRnBCK5FcnbdO8t1R3kQBL9cj9vhH7VOHOUVRnP3Wffo3esgWA7eKxdH18u9uXKWW0Yw1SR41A1Hk5zVsRE1R49gLnrREBLUEXFG6mjHR7Ueq1aSEYzgzU3GyS/7Lnm9T2TLHvnOSEYwgp+lKjk1+mmrZ9dDMIKfQWavK/2+7uh9Zufu778fwQheW9fN6jvOqttnnbd1VwhGcA2SW18fvTdqdFVptjs/GxEQjOBcrdqBMHq9qHVtOxtoL4Krnlab5dJnu2kEI3gvPeVJaQimdxKc5aKrnJN99XkRjOC9cu9sF11tP/JVVyqCEUwZ9Xs0uQhG8DMVRdyqOfPWnSAIRnCtnNJ7vWq9VK0n9/V+LwhGcA6x2S51dOd+NNF3n/3QKgQ/3VQei/cHRxOxy2pS1ilBCEYw7SwEc9E0I5dmzWUjGMFriLjqYtR7hWA6Cs5Fv4XMrJ4uBCN4T5dq5EAwgt9Qv1brb0YwCfDqkaFS77QAy8G0cz2MYATnutms+jebJDmY5ODIEUOZRAh+gnuNzt0IJgEmASYBJgHmotWno58n6yR6BL+1HDw22ZuUvftw9jMfEEzvIpgQTAIc6wl2cP4CrA5e44pb68cqZ0b2uuhZz1tCMBddo569Wnet/tzfqBktJ93RmhwcdVZk9Q6K1pFn9HtAMII3NQ+LXPPoGZfqYHo3wVe5eBbZUfVu9giCYHUw7SwEP1x/AF/o9pkbcr+pAAAAAElFTkSuQmCC",
    "dodge_l": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAADt0lEQVR42u3d246rMAyF4XZr3v+Vu69GIyFVHGInTvKty9FQAs7PsoOB9+v1+rxoOf1zCgSWJtLPbAP+fHKd4/1+I5bq6l01ecomc3WSEYvYvQidnWDEIhapM5GLWMQidSZyEYtYpM5ELmIXlcAKLPHYDb21mtci1qWYBJaGq1wHxV1vavXu3vtDLM1NbGv2+Lv9XZKe7ve4XVWCEYvYteq86OOoRi5iETtGRxKySe+9P8SSwJLALqvhHRStHvYtG71ab0bvXwcFrZ0Vz5aFWiumvTy2deafrfScEX+2Xeu4EEtre+xdErI87vd3Z7l7g1geW8Nbs70uy9vVsbS3xz4lt9dbZap7L2IR2yfrrZKlnnlldXIRi9g+WfJdgrPHNWtdi1jE9skqz8j8RvjVv1/d7mn9jVjas449kts7C23dX1bHBmIRm5vlfpupV4no1WHxNPu9u12v7B6xiyrs7s7TGd5aH0bN/Nan9aplzYhFbO6MjyI4O0turW95LI0l9u5KUasHVfuKR2u3ZBa5iEXsmHq3qlrHn12fIxaxtWd+1v9n16lZ5CIWsX2yursEZ69YtZJ69TxFn0/EIra2p2WvVT8df6/tELuJfnrPpFYv/B1Ha4dF9R6m1vON2F2JHUXqU6+8Os4j4VU6+4/jeHr+Ebu7x1ZXFc+MIr71CoLY3Yit4q1RBJx5aet+sr35bjwQy2Nziblbx2Zno08JrZJdI3YXYqt5xdkKU9RXQFoJ7VXXIhaxfTSqY7/191qvDKOqC8QiduxMzVrTzcq6R2fHiN2F2Ki7C1U9ehchdjePrUpudlYcXSePOl7E7poVjyY3u9Oh6jsRW58QQOzudew3clfLWkd7a9R5RezuxFb3pCjCRq1pR18BEYvYZ+Rmf32yWq/S3fORlaMgdlGFP9Ee/ZaYKr8b5dm9qgnEInash836NplR40YsYmkmIVYdu5+e+mWFe7mIRWwcAaNqOx5LiJ3Fc7qWGgX6phCL2DpZpysFYhG7Yv1ZrUcYsSSwva8EvvhMPFY9i1iqQGyVteEds2PEInae+pUQi9gZs9Fob0YsCSwJLAksCaysWH15PJ5ebz9HLP2Vaq8Cz+70fiIv+7sCiKW1iSXEksC2ef7smbzAqmPjsty79V+V9xo+zYpHfLMHsbLivPrw7L5n9W+/Rq1ARR4nYnls/Ew/bj9bx0L0eCO7KBGL2P4kVN9v5SsLYhHbLyv95l1ZJEfVq5WuVIhVx9JMQqzAksCSwJLAksCSwC6q/0t6j0gSsty0AAAAAElFTkSuQmCC",
    "dodge_r": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAADuElEQVR42u2d226EMAxEoer///L2aVUJCUHi2yQ+81g1S8A5GTsEOI/j+BxoO/1wCQgsIrCoWr+rdfjziU0JzvOEWKSrUzUrjiZzd5IhFmJ7Ebo6wRALsZC6ErkQC7GQuhK5EAuxkLoSuRC7qQgsgUV4bENvVfNaiGUqRgQWlUtuB8WoN1m9O/t4EIvWJtaaPX7bj5I0e9xrO1WCIRZi96rzvM9DjVyIhdgaXUmIJj37eBCLCCwisNuqfAeF1cPustG39ab38dlBgfbOilfLQlkrRr081jryn1Z6noh/amftF8SivT12lIQoj/v+7ip3byAWj9Xw1mivi/J26ljU22Nnyc16q4y690IsxOZkvSpZ6pNXqpMLsRCbkyWPEhzdr1XrWoiF2Jys8onMO8Lf/v1tu9n6G2JRzzr2Sm52Fmo9XtSODYiF2Ngs926kviUia4fFbPY72i4ru4fYTeV2d2d2hFvrQ6+Rb31aTy1rhliIjR3xXgRHZ8nW+haPRbXEjq4UWT1I7Sse1t2SUeRCLMTW1LuqsvY/uj6HWIjVHvlR/x9dp0aRC7EQm5PVjRIcvWJlJfXtdfK+nhALsdqeFr1WPdv/rHYQ20S/2SPJ6oXfflh3WKjvYbJeb4jtSmwVqbNe+bafV8JVdvZf+zF7/SG2u8eqS8UzvYi3ziAQ241YFW/1IuDJS63Hifbm0XhALB4bS8xoHRudjc4SqpJdQ2wXYtW84mmFyesrIFZCs+paiIXYHFXt2Lf+nnVmqKouIBZia0dq1JpuVNZdnR1DbBdive4uqHp0F0FsN49VJTc6K/auk6vOF2K7ZsXV5EbvdFB9J6L1CQGI7V7H3pG7W9Za7a1e1xViuxOr7klehFWtaXvPgBALsXPkRn99Um2v0uj1iMpRIHZTuT/R7v2WGJXf9fLsrGoCYiG21sNWfZtMVb8hFmJRi3Kng2anVYVbfkzFEOtHQFUJ0EkQC7H+pG6bkQpsr4FYiF2vmO82U0AsxK5df6ptJYVYRGCzZwI+DIzwWOpZiEUKxKqsDXfMjiEWYtepXxHEQuyK2ai3N0MsIrCIwCICiwgsWTH15fV8sl6SDbHov1Q7BB7xyH5wK/r18xCL9iYWQSwisDbPXz2TJ7DUsX5Z7mj9p/L6u9msuOLTLhBLVhxXHz7d91T/RKjXCpTneUIsHus/0q/tV9ux4N1fz12UEAux+SSoH1d5ZoFYiM3LSu+8K4pkr3pVaaaCWOpYtJIglsAiAosILCKwiMAiArup/gDZr49Ij9YnfQAAAABJRU5ErkJggg==",
    "blaster": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAD3UlEQVR42u2dSZbbMAwFrTytc+Isc+K+gLNyFnqt5oQPAlD9ZbdlcUARg2jqeL1e7xdKo18MQS6dWRr6fmsXguM4IAwJDCuaD1OTlJ08CIOw3ERFJw7CIKwmWVFIgzAIq03WbtIgDMKeQdYu0iAsmZgwJgyl9mHVfZe3L4MwlkTEhKH/CvPEeXTtX/WN3veDMAjLFU19rh+1/Lv7/n1/ffv3P8fvb6/bRRyEkYf9vPZb5ymrhN2RdUead/8gDMJyEtbyWa3/QxiCMHwYqk+YyhLvyOrNl3pJi0IWhEHYmq+xqu3NEubdfgiDsD2ktSx4lpjWdavt8hKEJVPYX2B6Vcc/3xulGg9h+DBtlKjyJSrfSZSIcvmwWdK8ThnY7dsgDMLWfM7uqK3li3aTBmEQNudzRolTtytqXgZhEDa39rdIuiOy9++9183mjxCGcuRhV9K8o7Io+VaaCcsuqwemYSas14K99kzMRoO7TsI5s1hWVrKs0xOzar31k2AvC7f69YsXmWcWy8pKlnW/twcdsz4kSm2xbJRYjbRRsqz6H/Z5mDdRWQzpVBHTKkFVjSLv+nNNZ2b7fWYfiKcpzEbSLBOy2v7VFYbiL4T5Wqrq8+o8a5Y0CKtOmCqfGiVOXdJaJat3nEbHE8KqEhbVZ6wWXVU/NFRdB2HJdKosxjpR/rRjdQtBtE01o+MNYVUIi1pdb9Xqeq+/9m/3pptrO+7GH8Kq+bDoiuKTrAhtEQ9h2QmL4rusLLblq1bvo/Z91/ZDGD5szMKtKxrWPqOXKK9oE8KyEua9Fo9+3mpPxGj0uOsJ+R2xEIYP01ii9Qqg3rGsirYh7OmEWVuWquanikLV0SKEZSWst1rsLTaQQlgtHxaVNHWUaJ3nqfoLYVWixN2kqZ8MRz3eobUjGMKq5WF3pFWL4nb7rt5xhbCqlY6oa74VEbtqnqMrFoRVJWyUNPXrp6LtxRgdj9lxgbBkkh9dtGpRu7/XyidarTgQ9lTCVBac9XQBVbshDMKQUhDGhKFQiXN1zQYPXsVjCIOwPsurfgwfhCEtYdUPZ75L8NX9hjAI00RhkA1hEBYhf4q2IRTCCOtRi9xIG4+YMHzYs6X2oRD2dMKi1A6rRosQhg/bk38R1iMI8/BZ1r4PwhATxoQhJgwxYUSJ5Eft/ngdbQthVdKXV7BXKqryL/UhzxCGYhGGIIwJe5Ki7d1gwsjDxqKw0fwlyiFds1Gi6gUFEPa0KHH1Bdi7XpVh1X7r74EwfJhN5SDaS0OtVobVcYAwCNNabvT77l4JIAzCbH2ZijyrfMubcAh7Wh6G8GHoB/0D4aHHSp2uhSsAAAAASUVORK5CYII=",
    "serious": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACMAQMAAACOMjPzAAAABlBMVEUAAAD///+l2Z/dAAABjElEQVRIx7XWsWolMQyF4R/UGvQqhm0H9OqCaQP3VQxuBWeLyWaTnRlPIOwpv8IuZIsDALg0+Jx/wSQpVxCSVCuQJGkBdkDegx8wfgJxQP0IBhK+AoiCBWwHbCsYUf4zcKiAsYBBBb4A0xz++jKXE/jwsQKfGq7XWMCQpH0F5lKxgtnBfAFWsdWMXIB8q6F9EOMMXnhqbLXLC9UZQsQIQVSkSWeQ0ur4QGpcA13p0qDM/ApGpg0AG7arzhDakyIbkYxrcPBUIXKjnaGzkVYxIo1+DY0091kYnX6GRiOtwRtGLiDyDQfyDAakVcwi7mGqxXyzCcYZSCj2mC0M2hV0SF4xKy3pV9AwmDFbUpZXYBmwx2zJq7gCYsIr5oT3V3cCDH7F/PUI2wNgHbuHQUgDv4c6Vpu4A973s9/DN2PZ7qGPJ8gD7B72xB6h5TdgPMPHGE5gDq0/wfYIvfO/QdA7FbcAUvqXJnCC76UtwIcAV9YdhAII+Z+LTyC9gKiPKnAB+V467mEmaOrvoZ/gN90MbCk6zT9iAAAAAElFTkSuQmCC",
    "laugh": "iVBORw0KGgoAAAANSUhEUgAAAHAAAACeAQMAAADQYBz6AAAABlBMVEUAAAD///+l2Z/dAAABj0lEQVRIx6XVsYrrMBCF4QPTGvQqAbeBefUBt4G8yoBawX8LxcmNLYXdrLoPzGgkHcnSX4dDTFkApgQ5OeFKo9BizJDVlC5DmmS3lJYhpf6xxiRF6NnHkRDOlGE0+YRNImUTpkRKM1qQ1+94lWWTxZgelk0+YeEe7mjC5uHbjH4nnFflAzeAMuF1cUib0G8hLT5hyVbr7dXVge1a6zajEbWWNqHohzbhp7Rb61eDIZ3Sp8sRIQAKbUCDViC9z3VgYfGQrF08RpQDe0gPdOQJ0Nd4YlAvDkY7E5K6OtzhRAPIWukbNCJAc4gBt+4CeWSBWs3cVhvzXlf31bYhW1nX1dYaQ2YxMzNLJ440KL2N+ljC/xT4znZmeTHPtL1UEmfqSdeArs64jLhIRmh/Nw9UT9Azwidu+/KGLNB8xnRAbcx+cZrG3NPwJcM/Mae0H5Ev+NiA0ISp15GciaSSMzbp9Yf5JT9WtiKpLBPqvcd3+tbfi8dUB9KapGdW3mlwlUTlcReO3PMy5l2yx4N05PfjH8unUJ4YhdbBAAAAAElFTkSuQmCC",
    "hurt": "iVBORw0KGgoAAAANSUhEUgAAAGQAAAB2CAYAAAA+/DbEAAADcklEQVR42u2dPXLjMAxG5UxusO2Wuf+JUqbdM3irNJrhEATxSz2UHsumRDwAH0hJr+u63hdWxj64BLXss+rA3m9fcF+vF4RgAkfJziHeJHQjB0KeTkg1IqoRAyFPJaQbGVmkQMjTCOlORjQpEPIUQk4jI4oUCClmTAgTgoXmkNNzh3cugRBCFsaEMCEYE8KEYEwIE1Kr3tfU/NrjmBCMCWFCsKm571z8jd/aHpdV/Lcah3evDkKqFS9X0IrhrqePPPP+u9LvZZ8PhJBDcjzMa7xUWeSQWp42q2pmhM2Oy676IIQckqMXpMRG6QoIIYfocod3LPdW5Ls5DkJOzyFWnqElJeouXe3/3HMVhDyFEOuYP/KkqOpn5sGrpOzqFAh5qg6R9rK0sddKl2gJlVZ9s+9BSFcdMpvhEQHSel5ava3+j/Q4rf5YJXl2HIR0yyFST9DG/PvvR/eYtP+nPd8ZYRDShRCrakfqgVEritpqyno8I1IgpEuV5aUHslfqvPSFdrwQ0o2QLKVc5oIsEmFNLoR00yFaTx95zr+/X6LvVXkqafR+Mgg5NYesVht3Uv78fKdcgNVem/c4IOR0QkZKWEuKVjd47YKHEAjx6fPPqpU7KavERHdtIQRC9qos7YqhlBjrPbpZpNDL6kLIbg/L6j4O69xSjZDZ+ULI6YR4Hz/SLdUI0UYMCDmNEKv1E6uVtygyvHpgEFLMyt5jKK1KrHTPKmk8yQFCck26F9c6J2QdDyEQIovJ0h6Vdq37V8fclX6Vri+EQEhMzpl5vrRHtkskhHRX6u/b1Gcp9dHvVal+vBU6hFQnJHodZFcpW3cEtGRZ5xYIOaXKkt4RFXUn1Op4pSRKOwNWZEPIaTnEOvZ3epOBxfVgTb06IddgX1aWR0cp4tWdlqvVmTYyQEhVQrR198yDvPZreRGijf1WK5UQ0l2HSNcpdpVw1efq7kYMdMhTlPrqip6Vos/eFeJFBoScRkh2rPeq0rLfngAhpxGy61nWSnk0Hu1dwlFVGkq9OiFWa9jRuWKXlBlBUeMkh5yeQ6xzjtczDlc/j64eIeR0QqLfJtDVeG5vV0KqVltVcx05hBxSS1dUJWg3d0BIN0LIJTkGId1yiBUpTyeMd1B1LRKuxXfh7j5b8RRPl57famSBkO6EjDzlaTnDq1cHIcXsP2vdhHJCgwA5AAAAAElFTkSuQmCC",
}
GASTER_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAFAAAAByAQMAAAD+u8TTAAAABlBMVEUAAAD///+l2Z/dAAAA/ElEQVQ4y6XUMarEMAwEUIFag65iSGvQ1QVuA76KwK1gtgiBlePPBv5Ur5hiqiH6M2z/pfiOGk86ASQL2RgwtkwhBYI8sxEAUMsMAQDXTFcACFkIhAKZjIuw35Sb/pt6MzIVoYiFcRU08x75gjJdQ0OGZ5qGBmfyNAl1HvZNcuuhnYUy+wwd/cEj9HxwHqHnWFinh8ooma16qJS2UCmUYqXABb6wXKyJrQiM4bV9k+WiW+IoMEadmThhjAMLXV1CMgkugAvoBdVLaJXIlKBaSD2TL1omgWoh0EKxWsVWkpcq9GAjahv2vmHpvW445oY8pm0IbEgAvebuSzb5AHEH2YB/GgUbAAAAAElFTkSuQmCC"
)

# Megalovania OST — SoundCloud timbre ref (Toby Fox); synth → base64 WAV (files = off)
SR = 22050
OST_BPM = 120.0

_NOTE = {
    "C": -9, "C#": -8, "Db": -8, "D": -7, "D#": -6, "Eb": -6, "E": -5, "F": -4,
    "F#": -3, "Gb": -3, "G": -2, "G#": -1, "Ab": -1, "A": 0, "A#": 1, "Bb": 1, "B": 2,
}


def _note_freq(name: str) -> float:
    octv = int(name[-1])
    key = name[:-1]
    return 440.0 * (2 ** ((_NOTE[key] + (octv - 4) * 12) / 12))


def _seq(text: str) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    for tok in text.split():
        if tok == "R":
            out.append(("R", 1.0))
        elif ":" in tok:
            note, beats = tok.split(":")
            out.append((note, float(beats)))
    return out


def _osc(wave: str, freq: float, t: float, duty: float = 0.5) -> float:
    phase = (t * freq) % 1.0
    if wave in ("sq", "pulse"):
        return 1.0 if phase < duty else -1.0
    if wave == "thin":
        return 1.0 if phase < 0.125 else -1.0
    if wave == "tri":
        return 4.0 * abs(phase - 0.5) - 1.0
    return random.uniform(-1.0, 1.0)


def _vib(freq: float, t: float, depth: float = 0.015, rate: float = 5.5) -> float:
    return freq * (1.0 + depth * math.sin(t * rate * math.tau))


def _kick(buf: list[float], pos: int, vol: float = 0.30) -> None:
    length = min(380, len(buf) - pos)
    for j in range(length):
        t = j / SR
        freq = 195.0 * (0.992 ** j)
        env = (1.0 - j / length) ** 2.2
        buf[pos + j] += math.sin(t * freq * math.tau) * vol * env


def _snare(buf: list[float], pos: int, vol: float = 0.10) -> None:
    length = min(220, len(buf) - pos)
    for j in range(length):
        env = (1.0 - j / length) ** 1.6
        tone = math.sin(j / SR * 185 * math.tau) * 0.35
        noise = (random.random() * 2.0 - 1.0) * 0.65
        buf[pos + j] += (tone + noise) * vol * env


def _hat(buf: list[float], pos: int, vol: float = 0.022) -> None:
    length = min(90, len(buf) - pos)
    for j in range(length):
        buf[pos + j] += (random.random() * 2.0 - 1.0) * vol * (1.0 - j / length)


def _pcm_to_wav(buf: list[float]) -> bytes:
    peak = max(abs(s) for s in buf) or 1.0
    pcm = array.array("h", (int(max(-1.0, min(1.0, s * 0.85 / peak)) * 32767) for s in buf))
    raw = pcm.tobytes()
    out = io.BytesIO()
    out.write(b"RIFF")
    out.write(struct.pack("<I", 36 + len(raw)))
    out.write(b"WAVEfmt ")
    out.write(struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16))
    out.write(b"data")
    out.write(struct.pack("<I", len(raw)))
    out.write(raw)
    return out.getvalue()


def _build_megalovania_wav() -> bytes:
    """D minor Megalovania loop — matches SoundCloud battle energy; no external files."""
    spb = 60.0 / OST_BPM
    melody = _seq(
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 F4:0.5 G4:0.5 A4:1 "
        "A4:0.5 Ab4:0.5 G4:1 D5:0.5 D5:0.5 D5:1 "
        "F4:0.5 G4:0.5 A4:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 F4:0.5 G4:0.5 A4:1 "
        "A4:0.5 Ab4:0.5 G4:2"
    )
    bass = _seq("D3:1 D3:1 A2:1 A2:1 D3:1 D3:1 F3:1 G3:1 A3:1 A3:1 D3:1 D3:1 F3:1 G3:1 A3:2")
    arp = (
        ("D4", "F4", "A4", "D5"),
        ("A3", "C4", "E4", "A4"),
        ("Bb3", "D4", "F4", "Bb4"),
        ("G3", "Bb3", "D4", "G4"),
    )
    total_beats = sum(beats for _, beats in melody)
    samples = int(total_beats * spb * SR)
    buf = [0.0] * samples

    pos = 0
    for note, beats in melody:
        note_samples = int(beats * spb * SR)
        if note != "R":
            freq = _note_freq(note)
            for i in range(note_samples):
                t = (pos + i) / SR
                env = min(1.0, i / 80.0) * (1.0 if i < note_samples - 400 else (note_samples - i) / 400.0)
                buf[pos + i] += _osc("pulse", _vib(freq, t), t, 0.25) * 0.24 * env
        pos += note_samples

    pos = 0
    bass_i = 0
    while pos < samples:
        note, beats = bass[bass_i % len(bass)]
        bass_i += 1
        note_samples = min(int(beats * spb * SR), samples - pos)
        freq = _note_freq(note)
        for i in range(note_samples):
            env = 1.0 if i < note_samples - 300 else (note_samples - i) / 300.0
            buf[pos + i] += _osc("tri", freq, (pos + i) / SR) * 0.20 * env
        pos += note_samples

    sixteenth = max(1, int(spb * SR / 4))
    arp_i = arp_t = 0
    for i in range(0, samples, sixteenth):
        chord = arp[arp_i % len(arp)]
        note = chord[arp_t % len(chord)]
        freq = _note_freq(note)
        for j in range(min(sixteenth, samples - i)):
            env = 1.0 if j < sixteenth - 80 else (sixteenth - j) / 80.0
            buf[i + j] += _osc("thin", freq, (i + j) / SR) * 0.09 * env
        arp_t += 1
        if arp_t % len(chord) == 0:
            arp_i += 1

    beat = int(spb * SR)
    i = beat_n = 0
    while i < samples:
        if beat_n % 4 in (0, 2):
            _kick(buf, i, 0.32)
        if beat_n % 4 in (1, 3):
            _snare(buf, i, 0.11)
        for h in range(2):
            _hat(buf, i + h * beat // 2)
        i += beat
        beat_n += 1

    return _pcm_to_wav(buf)


_OST_WAV_CACHE: bytes | None = None
_OST_B64_CACHE: str | None = None
_OST_LOCK = threading.Lock()


def _compose_ost_wav() -> bytes:
    global _OST_WAV_CACHE
    with _OST_LOCK:
        if _OST_WAV_CACHE is None:
            _OST_WAV_CACHE = _build_megalovania_wav()
        return _OST_WAV_CACHE


def prebuild_ost_async() -> None:
    """Synthesize the OST on a daemon thread at boot — first FIGHT is hitch-free."""
    threading.Thread(target=_compose_ost_wav, daemon=True).start()


def _compose_ost_b64() -> str:
    global _OST_B64_CACHE
    if _OST_B64_CACHE is None:
        _OST_B64_CACHE = base64.b64encode(_compose_ost_wav()).decode("ascii")
    return _OST_B64_CACHE


class LBMusic:
    """Megalovania — synth-built base64 WAV in RAM; starts on first FIGHT (files = off)."""

    def __init__(self) -> None:
        self.ok = False
        self.mute = MUTE
        self.playing = False
        self.sound: pygame.mixer.Sound | None = None
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(SR, -16, 1, 2048)
            wav = base64.b64decode(_compose_ost_b64())
            self.sound = pygame.mixer.Sound(io.BytesIO(wav))
            self.ok = True
        except (pygame.error, ValueError):
            self.sound = None

    def start_battle(self) -> None:
        """Begin looping battle OST — called when the player picks FIGHT the first time."""
        self._ensure_loaded()
        self.play_loop()

    def play_loop(self) -> None:
        if self.ok and self.sound and not self.mute and not self.playing:
            self.sound.play(-1)
            self.playing = True

    def stop(self) -> None:
        if self.sound:
            self.sound.stop()
            self.playing = False

    def toggle_mute(self) -> None:
        self.mute = not self.mute
        if not self.sound:
            return
        if self.mute:
            self.sound.stop()
            self.playing = False
        else:
            self.play_loop()


_LB_MUSIC: LBMusic | None = None


def get_music() -> LBMusic:
    global _LB_MUSIC
    if _LB_MUSIC is None:
        _LB_MUSIC = LBMusic()
    return _LB_MUSIC


class SansAnimator:
    """All Sans battle poses — real wiki sprites embedded as base64."""

    POSES = (
        "idle_0", "idle_1", "clenched", "fatal", "glow_0", "glow_1",
        "shrug", "point", "dodge_l", "dodge_r", "blaster", "serious", "laugh", "hurt",
    )

    def __init__(self) -> None:
        self.frames = {name: SpriteBank._from_b64(SANS_ANIMS_B64[name]) for name in self.POSES}
        self.pose = "shrug"
        self.tick = 0
        self.flash_pose: str | None = None
        self.flash_timer = 0

    def flash(self, pose: str, frames: int) -> None:
        self.flash_pose = pose
        self.flash_timer = frames

    def update(
        self,
        state: str,
        turn_timer: int,
        attack_pattern: int,
        blasters_firing: bool,
        player_hit: bool,
    ) -> None:
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.flash_pose = None
            return

        self.tick += 1
        if state == "INTRO":
            self.pose = "shrug"
        elif state in ("MENU", "SUBMENU"):
            self.pose = "idle_0" if (self.tick // 20) % 2 == 0 else "idle_1"
        elif state == "GAME_OVER":
            self.pose = "fatal"
        elif state == "PHASE_CLEAR":
            self.pose = "laugh"
        elif state == "SANS_TURN":
            if player_hit:
                self.pose = "hurt"
            elif turn_timer > 300:
                self.pose = "laugh"
            elif blasters_firing:
                self.pose = "glow_0" if (self.tick // 8) % 2 == 0 else "glow_1"
            elif attack_pattern == 0:
                self.pose = "point" if turn_timer > 60 else "clenched"
            elif attack_pattern == 1:
                self.pose = "blaster" if turn_timer > 30 else "serious"
            else:
                self.pose = "idle_0" if (self.tick // 20) % 2 == 0 else "idle_1"
        else:
            self.pose = "idle_0"

    def surface(self) -> pygame.Surface:
        key = self.flash_pose or self.pose
        return self.frames.get(key, self.frames["idle_0"])


class SpriteBank:
    """Undertale wiki sprites embedded as base64 — files = off."""

    def __init__(self) -> None:
        self.blaster = self._from_b64(GASTER_B64)
        self.sans_anim = SansAnimator()

    @staticmethod
    def _from_bytes(data: bytes) -> pygame.Surface:
        return pygame.image.load(io.BytesIO(data)).convert_alpha()

    @staticmethod
    def _from_b64(b64: str) -> pygame.Surface:
        return SpriteBank._from_bytes(base64.b64decode(b64))


_SPRITES: SpriteBank | None = None


def get_sprites() -> SpriteBank:
    global _SPRITES
    if _SPRITES is None:
        _SPRITES = SpriteBank()
    return _SPRITES


# --- INITIALIZATION ---
pygame.mixer.pre_init(SR, -16, 1, 2048)
pygame.init()
try:
    if not pygame.mixer.get_init():
        pygame.mixer.init(SR, -16, 1, 2048)
except pygame.error:
    pass
# SCALED: render at 640x480, GPU-scale to any window size — free resize, locked 60
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED, vsync=1)
except (pygame.error, TypeError):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("last breath 4k 0.2 — files = off")
clock = pygame.time.Clock()
FRAME = pygame.Surface((WIDTH, HEIGHT))  # single reusable frame buffer — no per-frame alloc

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)


def angle_diff_deg(a: float, b: float) -> float:
    d = math.degrees(a - b)
    return abs((d + 180) % 360 - 180)


_FONT_CACHE: dict[int, pygame.font.Font] = {}
_TEXT_CACHE: dict[tuple, pygame.Surface] = {}


def _font(size: int) -> pygame.font.Font:
    f = _FONT_CACHE.get(size)
    if f is None:
        f = _FONT_CACHE[size] = pygame.font.SysFont("impact", size)
    return f


def draw_text(surf, text, x, y, size, color, center=False):
    key = (text, size, color)
    rendered = _TEXT_CACHE.get(key)
    if rendered is None:
        if len(_TEXT_CACHE) > 512:  # bound the cache
            _TEXT_CACHE.clear()
        rendered = _TEXT_CACHE[key] = _font(size).render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(rendered, rect)


def draw_heart(surface, x, y, size, color):
    pygame.draw.polygon(
        surface,
        color,
        [(x, y + size // 4), (x + size // 2, y - size // 4), (x + size, y + size // 4), (x + size // 2, y + size)],
    )


def draw_lb_box(surface: pygame.Surface, box: pygame.Rect) -> None:
    pygame.draw.rect(surface, BLACK, box)
    pygame.draw.rect(surface, WHITE, box, 4)


def draw_lb_player_stats(surface: pygame.Surface, hp: int, max_hp: int, name: str = "FRISK", lv: int = 19) -> None:
    draw_text(surface, name, 38, STATS_Y, 20, WHITE)
    draw_text(surface, f"LV {lv}", 140, STATS_Y, 20, WHITE)
    draw_text(surface, "HP", 220, STATS_Y, 20, WHITE)
    bar_x, bar_y, bar_w, bar_h = 250, STATS_Y + 2, 120, 20
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_w, bar_h))
    fill = max(0, int(bar_w * hp / max_hp))
    pygame.draw.rect(surface, YELLOW, (bar_x, bar_y, fill, bar_h))
    draw_text(surface, f"{hp} / {max_hp}", bar_x + bar_w + 8, STATS_Y + 2, 16, WHITE)


def draw_lb_sans_header(surface: pygame.Surface, sans_rect: pygame.Rect, hp: int, max_hp: int) -> None:
    draw_text(surface, "SANS", SANS_X, sans_rect.top - 30, 22, WHITE, center=True)
    bar = pygame.Rect(SANS_X - 60, sans_rect.bottom + 6, 120, 8)
    pygame.draw.rect(surface, (60, 0, 0), bar)
    pygame.draw.rect(surface, RED, (bar.x, bar.y, max(1, int(bar.w * hp / max_hp)), bar.h))
    draw_text(surface, "ATK 1  DEF 1", SANS_X, bar.bottom + 6, 14, GRAY, center=True)


def draw_lb_menu(surface: pygame.Surface, box: pygame.Rect, sel: int, quote: str = "") -> None:
    if quote:
        draw_text(surface, quote, box.x + 14, box.y + 12, 15, GRAY)
    draw_text(surface, "What will you do?", box.x + 14, box.y + 36, 17, WHITE)
    for i, opt in enumerate(MENU_OPTS):
        col = YELLOW if i == sel else WHITE
        if opt == "MERCY" and sel != i:
            col = GRAY
        draw_text(surface, opt, box.x + 20 + i * 68, box.bottom - 34, 16, col)


def draw_lb_dialogue(surface: pygame.Surface, box: pygame.Rect, text: str) -> None:
    pygame.draw.rect(surface, BLACK, box)
    pygame.draw.rect(surface, WHITE, box, 4)
    words = text.split()
    line, y = "", box.y + 16
    for word in words:
        trial = (line + " " + word).strip()
        if len(trial) > 52:
            draw_text(surface, line, box.x + 14, y, 18, WHITE)
            y += 24
            line = word
        else:
            line = trial
    if line:
        draw_text(surface, line, box.x + 14, y, 18, WHITE)


class Player:
    def __init__(self):
        self.x = LB_BOX.centerx
        self.y = LB_BOX.centery + 30
        self.size = 16
        self.speed = 4
        self.hp = 92
        self.max_hp = 92
        self.invuln_timer = 0

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def move(self, keys, box):
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
        self.x = max(box.left + self.size // 2, min(box.right - self.size // 2, self.x + dx))
        self.y = max(box.top + self.size // 2, min(box.bottom - self.size // 2, self.y + dy))

    def draw(self, surface):
        if self.invuln_timer == 0 or self.invuln_timer % 4 < 2:
            draw_heart(surface, self.x, self.y, self.size, RED)


class Bone:
    def __init__(self, x, y, w, h, speed, direction):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.dir = direction

    def update(self):
        self.rect.x += self.speed * self.dir[0]
        self.rect.y += self.speed * self.dir[1]

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=3)


class GasterBlaster:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)
        self.timer = 0
        self.firing = False
        self.beam_x = x
        self.beam_y = y

    def mouth_pos(self):
        dist = 40
        return (
            self.x + math.cos(self.angle) * dist,
            self.y + math.sin(self.angle) * dist,
        )

    def update(self):
        self.timer += 1
        if self.timer == 30:
            self.firing = True
        if self.firing:
            self.beam_x, self.beam_y = self.mouth_pos()
        if self.timer > 90:
            self.firing = False

    _ROT_CACHE: dict[int, pygame.Surface] = {}
    _BEAM_CACHE: dict[int, pygame.Surface] = {}
    _BEAM_BASE: pygame.Surface | None = None

    @classmethod
    def _rotated(cls, deg: float) -> pygame.Surface:
        q = int(deg) % 360  # quantize to 1° — 360 max cached surfaces
        surf = cls._ROT_CACHE.get(q)
        if surf is None:
            surf = cls._ROT_CACHE[q] = pygame.transform.rotate(get_sprites().blaster, q)
        return surf

    @classmethod
    def _beam(cls, deg: float) -> pygame.Surface:
        q = int(deg) % 360
        surf = cls._BEAM_CACHE.get(q)
        if surf is None:
            if cls._BEAM_BASE is None:
                cls._BEAM_BASE = pygame.Surface((800, 20), pygame.SRCALPHA)
                cls._BEAM_BASE.fill((255, 255, 255, 200))
            surf = cls._BEAM_CACHE[q] = pygame.transform.rotate(cls._BEAM_BASE, q)
        return surf

    def draw(self, surface):
        bx, by = self.mouth_pos()
        rotated = self._rotated(-math.degrees(self.angle) - 90)
        surface.blit(rotated, rotated.get_rect(center=(int(bx), int(by))))
        if self.firing:
            beam = self._beam(-math.degrees(self.angle))
            surface.blit(beam, beam.get_rect(center=(int(bx), int(by))))


MAIN_MENU_OPTS = ("START", "MUTE", "QUIT")


class Game:
    def __init__(self):
        self.state = "MAINMENU"
        self.main_sel = 0
        self.menu_tick = 0
        self.dialogue = [
            "* LAST BREATH — PHASE 1",
            '* "you\'re not gonna give up, are you."',
            '* "on days like these, kids like you..."',
            '* "should be burning in hell."',
        ]
        self.dialogue_idx = 0
        self.battle_box = LB_BOX
        self.player = Player()
        self.bones: List[Bone] = []
        self.blasters: List[GasterBlaster] = []
        self.turn_timer = 0
        self.attack_pattern = 0
        self.sans_hp = 1
        self.sans_max_hp = 1
        self.shake = 0
        self.player_hit_flash = False
        self._menu_armed = False
        self.menu_sel = 0
        self.mercy = 0
        self.sans_turns = 0
        self.menu_quote = "* keeps staring."
        self.submenu_msg = ""
        self.submenu_timer = 0
        self.battle_music_started = False

    def reset_turn(self):
        self.bones.clear()
        self.blasters.clear()
        self.player.x = self.battle_box.centerx
        self.player.y = self.battle_box.centery + 30
        self.turn_timer = 0

    def handle_keydown(self, key: int) -> None:
        if self.state == "MAINMENU":
            if key in (pygame.K_UP, pygame.K_w):
                self.main_sel = (self.main_sel - 1) % len(MAIN_MENU_OPTS)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.main_sel = (self.main_sel + 1) % len(MAIN_MENU_OPTS)
            elif key in (pygame.K_z, pygame.K_RETURN):
                choice = MAIN_MENU_OPTS[self.main_sel]
                if choice == "START":
                    self.state = "INTRO"
                    self.dialogue_idx = 0
                elif choice == "MUTE":
                    get_music().toggle_mute()
                elif choice == "QUIT":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if key == pygame.K_ESCAPE:
            get_music().stop()
            self.__init__()  # back to main menu, fresh run
            return

        if self.state == "GAME_OVER":
            if key == pygame.K_r:
                get_music().stop()
                self.__init__()
                self.state = "INTRO"
            return

        if self.submenu_timer > 0:
            self.submenu_timer = 0
            self.submenu_msg = ""
            if self.state == "SUBMENU":
                self.state = "MENU"
            return

        if self.state == "INTRO":
            if key in (pygame.K_z, pygame.K_RETURN):
                self.dialogue_idx += 1
                if self.dialogue_idx >= len(self.dialogue):
                    self.state = "MENU"
                    self._menu_armed = True
            return

        if self.state == "MENU":
            if key in (pygame.K_LEFT, pygame.K_a):
                self.menu_sel = (self.menu_sel - 1) % len(MENU_OPTS)
                return  # cursor move must never select
            if key in (pygame.K_RIGHT, pygame.K_d):
                self.menu_sel = (self.menu_sel + 1) % len(MENU_OPTS)
                return
            if key not in (pygame.K_z, pygame.K_RETURN) or not self._menu_armed:
                return
            choice = MENU_OPTS[self.menu_sel]
            if choice == "FIGHT":
                if not self.battle_music_started:
                    self.battle_music_started = True
                    get_music().start_battle()
                self.state = "SANS_TURN"
                self.reset_turn()
                self.attack_pattern = random.randint(0, 1)
                self._menu_armed = False
            elif choice == "ACT":
                self.mercy = min(100, self.mercy + 15)
                self.submenu_msg = "* SANS — 1 ATK 1 DEF. The easiest enemy.\n* keeps dodging."
                self.state = "SUBMENU"
                self.submenu_timer = 90
            elif choice == "ITEM":
                self.submenu_msg = "* You have no items."
                self.state = "SUBMENU"
                self.submenu_timer = 60
            elif choice == "MERCY":
                if self.mercy >= 80:
                    self.state = "PHASE_CLEAR"
                else:
                    self.submenu_msg = "* SPARE was rejected."
                    self.state = "SUBMENU"
                    self.submenu_timer = 60
            return

        if self.state == "PHASE_CLEAR" and key in (pygame.K_z, pygame.K_RETURN, pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        keys = pygame.key.get_pressed()
        if self.shake > 0:
            self.shake -= 1

        if self.state == "MAINMENU":
            self.menu_tick += 1

        elif self.state == "SUBMENU":
            if self.submenu_timer > 0:
                self.submenu_timer -= 1
                if self.submenu_timer == 0:
                    self.submenu_msg = ""
                    self.state = "MENU"
                    self._menu_armed = True

        elif self.state == "SANS_TURN":
            self.player_hit_flash = False
            self.player.move(keys, self.battle_box)
            self.turn_timer += 1

            if self.attack_pattern == 0:
                if self.turn_timer % 20 == 0:
                    y_pos = random.randint(self.battle_box.y, self.battle_box.y + self.battle_box.h - 10)
                    self.bones.append(Bone(self.battle_box.right, y_pos, 20, 10, 4, (-1, 0)))
            elif self.attack_pattern == 1:
                if self.turn_timer % 60 == 0:
                    spawn_x = random.choice([self.battle_box.left, self.battle_box.right])
                    spawn_y = random.choice([self.battle_box.top, self.battle_box.bottom])
                    self.blasters.append(GasterBlaster(spawn_x, spawn_y, self.player.x, self.player.y))

            kill_zone = self.battle_box.inflate(120, 120)
            for b in self.bones[:]:
                b.update()
                if not kill_zone.colliderect(b.rect):  # works for every direction
                    self.bones.remove(b)
                if b.rect.colliderect(self.player.get_rect()) and self.player.invuln_timer == 0:
                    self.player.hp -= 5
                    self.player.invuln_timer = 30
                    self.shake = 10
                    self.player_hit_flash = True
                    get_sprites().sans_anim.flash("hurt", 8)

            for gb in self.blasters[:]:
                gb.update()
                if gb.firing:
                    p_rect = self.player.get_rect()
                    # perpendicular distance from player to the beam ray
                    dx, dy = p_rect.centerx - gb.beam_x, p_rect.centery - gb.beam_y
                    along = dx * math.cos(gb.angle) + dy * math.sin(gb.angle)
                    perp = abs(-dx * math.sin(gb.angle) + dy * math.cos(gb.angle))
                    if along > 0 and perp < 10 + self.player.size // 2 and self.player.invuln_timer == 0:
                        self.player.hp -= 8
                        self.player.invuln_timer = 30
                        self.shake = 15
                        self.player_hit_flash = True
                        get_sprites().sans_anim.flash("dodge_l", 10)
                if gb.timer > 90:
                    self.blasters.remove(gb)

            if self.turn_timer > 360:
                self.state = "MENU"
                self._menu_armed = True
                self.bones.clear()
                self.blasters.clear()
                self.player.x = self.battle_box.centerx
                self.player.y = self.battle_box.centery + 30
                self.sans_turns += 1
                self.menu_quote = random.choice([
                    "* you're going to have a bad time.",
                    "* keeps dodging.",
                    "* guess you really hate bad puns.",
                ])
                if self.sans_turns >= PHASE1_TURNS_TO_CLEAR:
                    self.state = "PHASE_CLEAR"

            if self.player.hp <= 0:
                self.state = "GAME_OVER"
                self.player.hp = 0
                get_music().stop()

        blasters_on = any(gb.firing for gb in self.blasters) if self.state == "SANS_TURN" else False
        get_sprites().sans_anim.update(
            self.state,
            self.turn_timer,
            self.attack_pattern,
            blasters_on,
            self.player_hit_flash,
        )

    def _draw_sans(self, temp_surf: pygame.Surface) -> pygame.Rect:
        sans_img = get_sprites().sans_anim.surface()
        sans_rect = sans_img.get_rect(center=(SANS_X, SANS_Y))
        temp_surf.blit(sans_img, sans_rect)
        draw_lb_sans_header(temp_surf, sans_rect, self.sans_hp, self.sans_max_hp)
        return sans_rect

    def _draw_main_menu(self, temp_surf: pygame.Surface) -> None:
        t = self.menu_tick
        # pulsing cyan back-glow behind Sans — pure procedural, files = off
        pulse = 0.5 + 0.5 * math.sin(t * 0.05)
        glow_r = int(70 + 26 * pulse)
        glow = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        for r in range(glow_r, 0, -6):
            a = int(4 + 26 * pulse * (1 - r / glow_r))
            pygame.draw.circle(glow, (51, 204, 255, a), (glow_r, glow_r), r)
        temp_surf.blit(glow, glow.get_rect(center=(WIDTH // 2, 190)))

        # Sans glow-eye idle pulled from the embedded base64 bank
        anim = get_sprites().sans_anim
        pose = "glow_0" if (t // 24) % 2 == 0 else "glow_1"
        img = anim.frames[pose]
        temp_surf.blit(img, img.get_rect(center=(WIDTH // 2, 190)))

        # flickering title
        flicker = 255 if random.random() > 0.03 else 140
        draw_text(temp_surf, "LAST BREATH", WIDTH // 2, 66, 52, (flicker, flicker, flicker), center=True)
        draw_text(temp_surf, "PHASE 1 — files = off", WIDTH // 2, 106, 16, (51, 204, 255), center=True)

        # options with heart cursor
        base_y = 330
        for i, opt in enumerate(MAIN_MENU_OPTS):
            label = opt
            if opt == "MUTE":
                label = "MUTE: ON" if get_music().mute else "MUTE: OFF"
            sel = i == self.main_sel
            col = YELLOW if sel else WHITE
            draw_text(temp_surf, label, WIDTH // 2, base_y + i * 34, 22, col, center=True)
            if sel:
                bob = int(2 * math.sin(t * 0.15))
                draw_heart(temp_surf, WIDTH // 2 - 90, base_y + i * 34 + 2 + bob, 14, RED)

        draw_text(temp_surf, "Z / ENTER select   ↑↓ move   M mute   F4 fullscreen",
                  WIDTH // 2, HEIGHT - 26, 14, GRAY, center=True)

    def draw(self, surface):
        shake_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        shake_y = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        temp_surf = FRAME  # reused buffer — zero per-frame surface allocation
        temp_surf.fill(BLACK)

        if self.state == "MAINMENU":
            self._draw_main_menu(temp_surf)

        elif self.state == "INTRO":
            self._draw_sans(temp_surf)
            if self.dialogue_idx < len(self.dialogue):
                draw_lb_dialogue(temp_surf, DLG_BOX, self.dialogue[self.dialogue_idx])
            draw_text(temp_surf, "[ Z ]", DLG_BOX.right - 36, DLG_BOX.bottom - 24, 14, GRAY)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        elif self.state in ("MENU", "SUBMENU"):
            self._draw_sans(temp_surf)
            draw_lb_box(temp_surf, self.battle_box)
            if self.state == "SUBMENU" and self.submenu_msg:
                for i, line in enumerate(self.submenu_msg.split("\n")):
                    draw_text(temp_surf, line, self.battle_box.x + 14, self.battle_box.y + 16 + i * 22, 16, WHITE)
                draw_text(temp_surf, "[ Z ]", self.battle_box.right - 36, self.battle_box.bottom - 24, 14, GRAY)
            else:
                draw_lb_menu(temp_surf, self.battle_box, self.menu_sel, self.menu_quote)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)
            if self.mercy > 0:
                draw_text(temp_surf, f"mercy {self.mercy}%", SANS_X, 188, 14, YELLOW, center=True)

        elif self.state == "SANS_TURN":
            self._draw_sans(temp_surf)
            draw_lb_box(temp_surf, self.battle_box)
            for b in self.bones:
                b.draw(temp_surf)
            for gb in self.blasters:
                gb.draw(temp_surf)
            self.player.draw(temp_surf)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        elif self.state == "GAME_OVER":
            self._draw_sans(temp_surf)
            draw_text(temp_surf, "GAME OVER", WIDTH // 2, HEIGHT // 2, 40, RED, center=True)
            draw_text(temp_surf, "Stay determined...", WIDTH // 2, HEIGHT // 2 + 50, 20, WHITE, center=True)
            draw_text(temp_surf, "[ R retry — ESC menu ]", WIDTH // 2, HEIGHT // 2 + 90, 16, GRAY, center=True)

        elif self.state == "PHASE_CLEAR":
            self._draw_sans(temp_surf)
            draw_text(temp_surf, "PHASE 1 CLEAR", WIDTH // 2, HEIGHT // 2 - 20, 36, YELLOW, center=True)
            draw_text(temp_surf, "* Sans vanishes into a pun.", WIDTH // 2, HEIGHT // 2 + 24, 18, WHITE, center=True)
            draw_text(temp_surf, "[ ESC or Z to quit ]", WIDTH // 2, HEIGHT // 2 + 64, 16, GRAY, center=True)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        surface.blit(temp_surf, (shake_x, shake_y))


def main():
    get_sprites()
    prebuild_ost_async()  # synth the OST off-thread while the menu shows
    music = get_music()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game.state == "MAINMENU":
                    running = False
                elif event.key == pygame.K_m:
                    music.toggle_mute()
                elif event.key == pygame.K_F4:
                    pygame.display.toggle_fullscreen()
                else:
                    game.handle_keydown(event.key)
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
