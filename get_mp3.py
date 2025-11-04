from pydub import AudioSegment
from pydub.generators import WhiteNoise

def noise_ver(path, try_num, vol=35):
    sound = AudioSegment.from_file(path)

    # 최초 음원이라면, 빠르기 조절
    if path[:1] != 'noise':
        faster = sound.speedup(playback_speed=1.4)

    # 피치 조절 (중간 톤 높이기 → 날카로운 기계 톤)
    higher = faster._spawn(faster.raw_data, overrides={
        "frame_rate": int(faster.frame_rate * 1.5)
    }).set_frame_rate(faster.frame_rate)

    # 약간 디지털 느낌 주기 (volume 줄이고 distortion 느낌)
    higher = higher - 5

    # 화이트 노이즈 생성
    noise = WhiteNoise().to_audio_segment(duration=len(higher), volume=(-1) * vol)

    # 원본 음성과 노이즈 합치기
    robotic = higher.overlay(noise)

    # MP3로 저장
    output_path = str(try_num)+'_noise_'+path
    robotic.export(output_path, format="mp3")

    return output_path