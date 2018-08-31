import sys, os, re, shutil
from os.path import join
import argparse

class ExtractFiles:
    LAST_MONTH_FILE_NAME = ".last_month"

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("copyto", help = "directory path of copy to", type = str)
        parser.add_argument("--all", help = "Optional このオプションを付与するとすべてのファイルを抽出対象にします", action = "store_true")

        return parser.parse_args()


    def __getLastCopiedPair(self, lastMonthFile, isAll):
        if isAll:
            return (1, 1)

        try:
            with open(lastMonthFile, mode='r') as f:
                line = f.readline()
                print("read .last_month is", line)
                return tuple(list(map(lambda s: int(s), line.split("-"))))

        except FileNotFoundError:
            print("no .last_month")
            return (1, 1)  # 1年1月


    def extract(self, copyto, isAll=False):
        rootPath = os.getcwd()

        if not os.path.isdir(copyto):
            os.makedirs(copyto)

        lastMonthFile = join(copyto, self.LAST_MONTH_FILE_NAME)

        lastCopied = self.__getLastCopiedPair(lastMonthFile, isAll)

        cnt = 0
        lastMonth = ""

        # year
        for year in list( \
                    filter( \
                        lambda yearDir: re.match("^20[0-9]{2}$", yearDir) and lastCopied[0] <= int(yearDir), os.listdir(rootPath) \
                    )):
            # month
            for month in list( \
                         filter( \
                            lambda monthDir: re.match("^[0-9]{2}$", monthDir) and lastCopied[1] <= int(monthDir), os.listdir(join(rootPath, year)) \
                         )):
                for root, dirs, files in os.walk(join(rootPath, year, month)):
                    if len(files) != 0:
                        lastMonth = year + '-' + month
                        for file in list( \
                                    filter( \
                                        lambda file: re.match("^[^.].*", file), files \
                                    )):
                            print("copy", join(root,file), "to", join(copyto, year, month, file))
                            if not os.path.isdir(join(copyto, year, month)):
                                print("There is no", join(copyto, year, month), "then, makedirs()")
                                os.makedirs(join(copyto, year, month))
                            shutil.copy2(join(root,file), join(copyto, year, month, file))
                            cnt += 1
        else:
            print("copied", cnt, "files")
            print("last copied month is", lastMonth)
            with open(lastMonthFile, mode='w') as f:
                f.write(lastMonth)

if __name__ == "__main__":
    
    extractor = ExtractFiles()
    args = extractor.get_args()
    print(args)
    extractor.extract(args.copyto, args.all)
