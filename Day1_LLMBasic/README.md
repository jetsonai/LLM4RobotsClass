# 실습환경
Google Colab

## for local colab docker image
- change docker base path
  ```
  sudo vim /etc/docker/daemon.json
  {
      "data-root": "NEW_PATH/docker"
  }
  ```

- google colab docker
  ```
  docker run --runtime nvidia -e NVIDIA_DRIVER_CAPABILITIES=all -e NVIDIA_VISIBLE_DEVICES=all --net=host --ipc=host --privileged -v /mnt/hdd/workspace:/content/workspace -v /mnt/hdd/root:/root --rm asia-docker.pkg.dev/colab-images/public/runtime
  ```

# 개요

## 자연어 처리 개요
강의자료

## 전처리
강의자료와 노트북

01_전처리_데이터_클리닝

02_전처리_토큰화

03_전처리_정규화

04_전처리_불용어제거

05_전처리_텍스트_벡터화

## 딥 러닝을 이용한 자연어 처리
강의자료와 노트북

06_LSTM_실습

07_Seq2Seq_실습

08_Attention_실습

09_Transformer_t실습

10_BERT_실습

11_GPT_실습

12_LLAMA_실습

13_EXAONE_실습

## 파인 튜닝과 프롬프트 튜닝
강의자료

14_프롬프트_튜닝_실습
